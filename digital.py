from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="DIGITAL GROWTH STUDIO")

app.mount("/static", StaticFiles(directory="static"), name="static")

def connect():
    return sqlite3.connect("agency.db")

def setup_database():
    con = connect()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        business TEXT,
        phone TEXT,
        email TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        title TEXT,
        service TEXT,
        fee REAL,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        amount REAL,
        date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        amount REAL
    )
    """)

    con.commit()
    con.close()

setup_database()


class Client(BaseModel):
    name: str
    business: str = ""
    phone: str = ""
    email: str = ""


class Project(BaseModel):
    client_id: int
    title: str
    service: str
    fee: float
    status: str = "Pending"


class Payment(BaseModel):
    client_id: int
    amount: float
    date: str


class Expense(BaseModel):
    title: str
    amount: float


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/clients")
def get_clients():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM clients")
    data = cur.fetchall()
    con.close()
    return data


@app.post("/clients")
def add_client(client: Client):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO clients(name,business,phone,email) VALUES(?,?,?,?)",
        (client.name, client.business, client.phone, client.email)
    )
    con.commit()
    con.close()
    return {"message": "Client added successfully"}


@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM clients WHERE id=?", (client_id,))
    con.commit()
    con.close()
    return {"message": "Client deleted"}


@app.get("/projects")
def get_projects():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM projects")
    data = cur.fetchall()
    con.close()
    return data


@app.post("/projects")
def add_project(project: Project):
    con = connect()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO projects(client_id,title,service,fee,status) VALUES(?,?,?,?,?)",
        (
            project.client_id,
            project.title,
            project.service,
            project.fee,
            project.status
        )
    )

    con.commit()
    con.close()
    return {"message": "Project created"}


@app.post("/payments")
def add_payment(payment: Payment):
    con = connect()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO payments(client_id,amount,date) VALUES(?,?,?)",
        (payment.client_id, payment.amount, payment.date)
    )

    con.commit()
    con.close()
    return {"message": "Payment saved"}


@app.post("/expenses")
def add_expense(expense: Expense):
    con = connect()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO expenses(title,amount) VALUES(?,?)",
        (expense.title, expense.amount)
    )

    con.commit()
    con.close()
    return {"message": "Expense saved"}


@app.get("/dashboard")
def dashboard():
    con = connect()
    cur = con.cursor()

    clients = cur.execute(
        "SELECT COUNT(*) FROM clients"
    ).fetchone()[0]

    projects = cur.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    revenue = cur.execute(
        "SELECT COALESCE(SUM(amount),0) FROM payments"
    ).fetchone()[0]

    expenses = cur.execute(
        "SELECT COALESCE(SUM(amount),0) FROM expenses"
    ).fetchone()[0]

    fees = cur.execute(
        "SELECT COALESCE(SUM(fee),0) FROM projects"
    ).fetchone()[0]

    con.close()

    return {
        "clients": clients,
        "projects": projects,
        "revenue": revenue,
        "expenses": expenses,
        "pending": max(fees - revenue, 0),
        "profit": revenue - expenses
    }
