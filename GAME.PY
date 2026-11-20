"""
================================================================================
PROJECT TITLE  : CYBER VAULT - TERMINAL CODEBREAKER
PROGRAMMING    : Python 3
TYPE           : Interactive Static Console Mini-Project Game
AUTHOR         : Python Mini Project Student
================================================================================
"""

import os
import sys
import time
import random

# ==============================================================================
# 1. COLOR & FORMATTING CONSTANTS (ANSI Escape Codes)
# ==============================================================================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

BG_BLUE = "\033[44m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"


def enable_windows_ansi():
    """Enables virtual terminal processing on Windows if supported."""
    if os.name == 'nt':
        os.system('')


enable_windows_ansi()

# ==============================================================================
# 2. GLOBAL GAME CONFIGURATION & STATISTICS
# ==============================================================================
session_stats = {
    "games_played": 0,
    "games_won": 0,
    "games_lost": 0,
    "best_score": None,      # Fewest attempts used to win
    "total_hints_used": 0
}

DIFFICULTY_PRESETS = {
    "1": {"name": "Cadet (Easy)", "code_len": 3, "max_attempts": 8},
    "2": {"name": "Operative (Medium)", "code_len": 4, "max_attempts": 7},
    "3": {"name": "Cyber Master (Hard)", "code_len": 5, "max_attempts": 6}
}

current_difficulty = "2"  # Default: Operative (Medium, 4 digits, 7 attempts)


# ==============================================================================
# 3. HELPER & UI DISPLAY FUNCTIONS
# ==============================================================================
def clear_screen():
    """Clears the terminal screen cleanly for Windows and Unix-like OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_divider(char="=", length=65, color=CYAN):
    """Prints a styled divider line."""
    print(f"{color}{char * length}{RESET}")


def print_banner():
    """Displays the ASCII title banner."""
    banner = f"""
{CYAN}{BOLD}
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██║   ██║███████║██║   ██║██║     ██║   
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   
╚██████╗   ██║   ██████╔╝███████╗██║  ██║     ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   
{RESET}
{YELLOW}             >> SECURE TERMINAL CODEBREAKER SYSTEM v2.5 <<{RESET}
"""
    print(banner)


def show_instructions():
    """Displays comprehensive game instructions, rules, and logic."""
    clear_screen()
    print_divider("=", 65, CYAN)
    print(f"{BOLD}{WHITE}                   HOW TO PLAY - GAME RULES{RESET}")
    print_divider("=", 65, CYAN)
    print(f"""
{BOLD}{YELLOW}OBJECTIVE:{RESET}
You are an elite cyber agent tasked with breaking into an encrypted
vault. The vault security engine generates a secret multi-digit PIN.
Your mission is to deduce the exact secret passcode before you run out
of security bypass attempts.

{BOLD}{YELLOW}RULE SET & FEEDBACK MECHANISM:{RESET}
1. {WHITE}Each digit in the secret code is unique (e.g., '4819' or '270').{RESET}
2. After entering each guess, the terminal analyzes your input:
   - {GREEN}{BOLD}EXACT HIT [●]{RESET} : Digit exists AND is in the {GREEN}correct position{RESET}.
   - {YELLOW}{BOLD}NEAR HIT  [○]{RESET} : Digit exists in code BUT in the {YELLOW}wrong position{RESET}.
   - {RED}{BOLD}MISS      [X]{RESET} : Digit does not exist anywhere in the code.
3. {WHITE}Example:{RESET} If the secret is {BOLD}5821{RESET} and you guess {BOLD}5298{RESET}:
   - '5' is exact match (Pos 1)      -> {GREEN}1 Exact Hit{RESET}
   - '2' and '8' exist elsewhere     -> {YELLOW}2 Near Hits{RESET}
   - '9' is not in the secret code   -> {RED}1 Miss{RESET}
4. {WHITE}Lifeline (Hint):{RESET} Type {CYAN}'hint'{RESET} once during a round for a clue.
5. {WHITE}Surrender:{RESET} Type {RED}'exit'{RESET} at any time to abort the hack.
""")
    print_divider("-", 65, BLUE)
    input(f"{CYAN}Press Enter to return to Main Menu...{RESET}")


def show_statistics():
    """Displays user performance statistics and win rate."""
    clear_screen()
    print_divider("=", 65, CYAN)
    print(f"{BOLD}{WHITE}                 AGENT PERFORMANCE DOSSIER{RESET}")
    print_divider("=", 65, CYAN)

    games = session_stats["games_played"]
    wins = session_stats["games_won"]
    losses = session_stats["games_lost"]
    hints = session_stats["total_hints_used"]
    best = session_stats["best_score"]

    win_rate = (wins / games * 100) if games > 0 else 0.0

    print(f"\n  {WHITE}Total Missions Conducted :{RESET} {BOLD}{CYAN}{games}{RESET}")
    print(f"  {WHITE}Successful Vault Breaches:{RESET} {BOLD}{GREEN}{wins}{RESET}")
    print(f"  {WHITE}Security Lockouts (Fails):{RESET} {BOLD}{RED}{losses}{RESET}")
    print(f"  {WHITE}Operational Win Rate     :{RESET} {BOLD}{YELLOW}{win_rate:.1f}%{RESET}")
    print(f"  {WHITE}Fewest Attempts to Breach:{RESET} {BOLD}{MAGENTA}{best if best is not None else 'N/A'}{RESET}")
    print(f"  {WHITE}Security Hints Requested :{RESET} {BOLD}{WHITE}{hints}{RESET}\n")

    print_divider("-", 65, BLUE)
    input(f"{CYAN}Press Enter to return to Main Menu...{RESET}")


def change_difficulty():
    """Allows user to select and update the game difficulty level."""
    global current_difficulty
    while True:
        clear_screen()
        print_divider("=", 65, CYAN)
        print(f"{BOLD}{WHITE}                   SECURITY CLEARANCE LEVEL{RESET}")
        print_divider("=", 65, CYAN)
        print(f"\nCurrent Active Difficulty: {BOLD}{YELLOW}{DIFFICULTY_PRESETS[current_difficulty]['name']}{RESET}\n")

        for key, val in DIFFICULTY_PRESETS.items():
            active_marker = f"{GREEN}[ACTIVE]{RESET}" if key == current_difficulty else ""
            print(f"  [{key}] {val['name']} -> {val['code_len']} Digits | {val['max_attempts']} Attempts {active_marker}")

        print(f"  [B] Back to Main Menu")
        print_divider("-", 65, BLUE)

        choice = input(f"{BOLD}{CYAN}Select Clearance Level (1/2/3/B): {RESET}").strip().upper()

        if choice in DIFFICULTY_PRESETS:
            current_difficulty = choice
            print(f"\n{GREEN}Difficulty updated to: {DIFFICULTY_PRESETS[choice]['name']}!{RESET}")
            time.sleep(1.2)
            break
        elif choice == 'B':
            break
        else:
            print(f"\n{RED}Invalid selection. Please choose 1, 2, 3, or B.{RESET}")
            time.sleep(1.2)


# ==============================================================================
# 4. CORE GAME ENGINE LOGIC
# ==============================================================================
def generate_secret_code(length):
    """Generates a list of unique randomized digits as strings."""
    digits = [str(n) for n in range(10)]
    return random.sample(digits, length)


def evaluate_guess(secret_code, guess):
    """Compares the user's guess against the secret code."""
    exact_hits = 0
    near_hits = 0

    for i in range(len(secret_code)):
        if guess[i] == secret_code[i]:
            exact_hits += 1
        elif guess[i] in secret_code:
            near_hits += 1

    return exact_hits, near_hits


def provide_clue(secret_code):
    """Generates an intelligent mathematical clue for the player."""
    clue_type = random.choice(["sum", "parity", "contains"])
    digits_int = [int(d) for d in secret_code]

    if clue_type == "sum":
        total_sum = sum(digits_int)
        return f"Sum of all digits in the code equals {BOLD}{YELLOW}{total_sum}{RESET}."
    elif clue_type == "parity":
        evens = sum(1 for d in digits_int if d % 2 == 0)
        odds = len(digits_int) - evens
        return f"The code contains {BOLD}{YELLOW}{evens} Even{RESET} and {BOLD}{YELLOW}{odds} Odd{RESET} digits."
    else:
        sample_digit = random.choice(secret_code)
        return f"Telemetry confirmed: The code definitely contains the digit {BOLD}{YELLOW}'{sample_digit}'{RESET}."


def play_game():
    """Executes a complete single round of Cyber Vault."""
    config = DIFFICULTY_PRESETS[current_difficulty]
    code_length = config["code_len"]
    max_attempts = config["max_attempts"]

    secret_code = generate_secret_code(code_length)

    attempts_history = []
    attempts_remaining = max_attempts
    hint_available = True
    round_won = False
    attempts_used = 0

    clear_screen()
    print_divider("=", 65, CYAN)
    print(f"{BOLD}{WHITE}              VAULT PENETRATION SEQUENCE INITIALIZED{RESET}")
    print_divider("=", 65, CYAN)
    print(f"  {WHITE}Clearance Level :{RESET} {BOLD}{YELLOW}{config['name']}{RESET}")
    print(f"  {WHITE}Passcode Specs  :{RESET} {BOLD}{GREEN}{code_length} UNIQUE Digits (0-9){RESET}")
    print(f"  {WHITE}Security Buffer :{RESET} {BOLD}{RED}{max_attempts} Failed Attempts Allowed{RESET}")
    print(f"  {WHITE}Commands        :{RESET} Type {CYAN}'hint'{RESET} for clue | {RED}'exit'{RESET} to abort")
    print_divider("-", 65, BLUE)

    # Main Guessing Loop
    while attempts_remaining > 0:
        print(f"\n{BOLD}{WHITE}[ Attempt {attempts_used + 1}/{max_attempts} ]  Remaining Tries: {RED}{attempts_remaining}{RESET}")

        user_input = input(f"{BOLD}{CYAN}Enter {code_length}-Digit Guess >> {RESET}").strip()

        # Check for surrender
        if user_input.lower() == 'exit':
            print(f"\n{RED}Mission aborted by operative. Self-destructing session...{RESET}")
            time.sleep(1.5)
            session_stats["games_played"] += 1
            session_stats["games_lost"] += 1
            return

        # Check for hint
        if user_input.lower() == 'hint':
            if hint_available:
                hint_available = False
                session_stats["total_hints_used"] += 1
                clue = provide_clue(secret_code)
                print(f"\n{BG_BLUE}{WHITE} INTEL INTERCEPT {RESET} {clue}")
            else:
                print(f"\n{YELLOW}>> Satellite Uplink Exhausted: You have already used your hint!{RESET}")
            continue

        # Input Validation (No crash, no attempt penalty)
        if not user_input.isdigit():
            print(f"{RED}>> ERROR: Passcode must contain digits (0-9) only. Non-numeric input ignored.{RESET}")
            continue

        if len(user_input) != code_length:
            print(f"{RED}>> ERROR: Code must be exactly {code_length} digits long. (You entered {len(user_input)}){RESET}")
            continue

        if len(set(user_input)) != len(user_input):
            print(f"{RED}>> ERROR: All digits must be unique. No duplicate digits allowed in passcode.{RESET}")
            continue

        # Process valid guess
        attempts_used += 1
        attempts_remaining -= 1
        guess_digits = list(user_input)

        exact_hits, near_hits = evaluate_guess(secret_code, guess_digits)

        attempts_history.append({
            "attempt": attempts_used,
            "guess": user_input,
            "exact": exact_hits,
            "near": near_hits
        })

        # Display Turn Feedback Table
        print(f"\n{BOLD}{WHITE}--- HACK LOG & TELEMETRY ---{RESET}")
        print(f"{'ROUND':<8}{'GUESS':<12}{'EXACT [●]':<14}{'NEAR [○]':<14}")
        print("-" * 48)
        for entry in attempts_history:
            exact_colored = f"{GREEN}{entry['exact']} Exact{RESET}" if entry['exact'] > 0 else f"{DIM}0 Exact{RESET}"
            near_colored = f"{YELLOW}{entry['near']} Near{RESET}" if entry['near'] > 0 else f"{DIM}0 Near{RESET}"
            print(f"{entry['attempt']:<8}{entry['guess']:<12}{exact_colored:<23}{near_colored:<23}")
        print("-" * 48)

        # Check victory
        if exact_hits == code_length:
            round_won = True
            break

    # Outcome handling
    session_stats["games_played"] += 1

    if round_won:
        session_stats["games_won"] += 1
        if session_stats["best_score"] is None or attempts_used < session_stats["best_score"]:
            session_stats["best_score"] = attempts_used

        score = (max_attempts - attempts_used + 1) * 250
        print(f"\n{BG_GREEN}{WHITE}{BOLD}                 ACCESS GRANTED! VAULT DECRYPTED!                {RESET}")
        print(f"\n{GREEN}{BOLD}Congratulations, Agent!{RESET}")
        print(f"You cracked the secret cipher {BOLD}{CYAN}{''.join(secret_code)}{RESET} in {BOLD}{attempts_used}{RESET} attempts.")
        print(f"Mission Efficiency Score: {BOLD}{YELLOW}{score} Points{RESET}\n")
    else:
        session_stats["games_lost"] += 1
        print(f"\n{BG_RED}{WHITE}{BOLD}               SECURITY LOCKDOWN! CONNECTION TERMINATED!          {RESET}")
        print(f"\n{RED}{BOLD}Mission Failed!{RESET} You ran out of security bypass attempts.")
        print(f"The actual secret vault passcode was: {BOLD}{YELLOW}{''.join(secret_code)}{RESET}\n")

    print_divider("=", 65, CYAN)
    input(f"{CYAN}Press Enter to proceed...{RESET}")


# ==============================================================================
# 5. MAIN PROGRAM LOOP & CONTROLLER
# ==============================================================================
def main():
    """Main application loop displaying the menu and managing user selections."""
    while True:
        clear_screen()
        print_banner()

        active_diff_name = DIFFICULTY_PRESETS[current_difficulty]["name"]
        print(f"  {WHITE}Active Clearance Level : {BOLD}{YELLOW}{active_diff_name}{RESET}")
        print(f"  {WHITE}Total Missions Breached: {BOLD}{GREEN}{session_stats['games_won']}/{session_stats['games_played']}{RESET}\n")

        print_divider("-", 65, CYAN)
        print(f"  {BOLD}{WHITE}[1] START VAULT BREACH MISSION{RESET}")
        print(f"  {BOLD}{WHITE}[2] HOW TO PLAY & CIPHER RULES{RESET}")
        print(f"  {BOLD}{WHITE}[3] CHANGE DIFFICULTY LEVEL{RESET}")
        print(f"  {BOLD}{WHITE}[4] VIEW AGENT PERFORMANCE DOSSIER{RESET}")
        print(f"  {BOLD}{WHITE}[5] EXIT TERMINAL{RESET}")
        print_divider("-", 65, CYAN)

        choice = input(f"\n{BOLD}{CYAN}Select Option (1-5): {RESET}").strip()

        if choice == "1":
            play_game()
        elif choice == "2":
            show_instructions()
        elif choice == "3":
            change_difficulty()
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            clear_screen()
            print_divider("=", 65, CYAN)
            print(f"\n{BOLD}{GREEN}Thank you for playing CYBER VAULT. Agent session closed.{RESET}\n")
            print_divider("=", 65, CYAN)
            break
        else:
            print(f"\n{RED}Invalid entry '{choice}'. Please select a number between 1 and 5.{RESET}")
            time.sleep(1.2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Process interrupted by user. Exiting Cyber Vault...{RESET}")
        sys.exit(0)