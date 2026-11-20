
================================================================================
PROJECT TITLE  : COSMIC DEFENDER - GALAXY STRIKE
DEVELOPED WITH : Python 3 & Pygame 2D Engine
TYPE           : Real-Time Graphical Arcade Mini-Project
AUTHOR         : Python Mini Project Student
================================================================================
"""

import sys
import math
import random
import pygame
import numpy as np

# ==============================================================================
# 1. INITIALIZATION & DISPLAY CONSTANTS
# ==============================================================================
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("COSMIC DEFENDER: GALAXY STRIKE")
clock = pygame.time.Clock()

# Color Palette (RGB)
COLOR_BG = (10, 14, 26)
COLOR_WHITE = (255, 255, 255)
COLOR_CYAN = (0, 240, 255)
COLOR_NEON_BLUE = (30, 144, 255)
COLOR_YELLOW = (255, 220, 0)
COLOR_RED = (255, 50, 70)
COLOR_GREEN = (40, 240, 100)
COLOR_PURPLE = (180, 70, 255)
COLOR_ORANGE = (255, 140, 20)
COLOR_DARK_GRAY = (40, 45, 60)

# Fonts
font_title = pygame.font.SysFont("impact", 54)
font_large = pygame.font.SysFont("arial", 28, bold=True)
font_medium = pygame.font.SysFont("arial", 20, bold=True)
font_small = pygame.font.SysFont("consolas", 15, bold=True)

# ==============================================================================
# 2. SYNTHESIZED RETRO SOUND EFFECTS (Pure Code Generation)
# ==============================================================================
class DummySound:
    def play(self):
        pass


def generate_synthesized_sounds():
    """Generates retro arcade waveforms dynamically using NumPy without external audio files."""
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        sample_rate = 44100

        # Laser Sound (Frequency sweep down)
        dur = 0.09
        t = np.linspace(0, dur, int(sample_rate * dur), False)
        freq = np.linspace(950, 280, len(t))
        wave = (np.sin(2 * np.pi * freq * t) * 12000 * np.linspace(1, 0, len(t))).astype(np.int16)
        snd_laser = pygame.sndarray.make_sound(np.column_stack((wave, wave)))

        # Explosion Sound (White noise with decay)
        dur = 0.35
        t = np.linspace(0, dur, int(sample_rate * dur), False)
        noise = (np.random.uniform(-1, 1, len(t)) * 14000 * (np.exp(-7 * t))).astype(np.int16)
        snd_explosion = pygame.sndarray.make_sound(np.column_stack((noise, noise)))

        # Power-Up Chime (Ascending tone)
        dur = 0.22
        t = np.linspace(0, dur, int(sample_rate * dur), False)
        freq = np.linspace(440, 880, len(t))
        wave = (np.sin(2 * np.pi * freq * t) * 13000 * np.linspace(1, 0.2, len(t))).astype(np.int16)
        snd_powerup = pygame.sndarray.make_sound(np.column_stack((wave, wave)))

        # Player Hurt Buzz
        dur = 0.15
        t = np.linspace(0, dur, int(sample_rate * dur), False)
        wave = (np.sign(np.sin(2 * np.pi * 110 * t)) * 10000 * np.linspace(1, 0, len(t))).astype(np.int16)
        snd_hit = pygame.sndarray.make_sound(np.column_stack((wave, wave)))

        return snd_laser, snd_explosion, snd_powerup, snd_hit
    except Exception:
        return DummySound(), DummySound(), DummySound(), DummySound()


SND_LASER, SND_EXPLOSION, SND_POWERUP, SND_HIT = generate_synthesized_sounds()

# ==============================================================================
# 3. GAME OBJECT CLASSES
# ==============================================================================
class Star:
    """Parallax scrolling background star."""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.layer = random.choice([1, 2, 3])
        self.speed = self.layer * 0.9
        self.radius = self.layer
        self.color = (180, 200, 255) if self.layer == 3 else (