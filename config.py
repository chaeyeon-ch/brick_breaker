import pygame
import math
from array import array

# Screen settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ROW_COLORS = [
    (255, 0, 0),     # red
    (255, 165, 0),   # orange
    (255, 255, 0),   # yellow
    (0, 128, 0),     # green
    (0, 0, 255)      # blue
]

# Brick settings
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 7

# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 5

# Sound placeholders
SOUND_ENABLED = False
HIT_PADDLE_SOUND = None
HIT_BRICK_SOUND = None
VICTORY_SOUND = None
GAME_OVER_SOUND = None

def generate_tone(frequency=440, duration_ms=150, volume=0.5):
    """Generate a simple sine wave tone."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = array('h')
    amplitude = int(32767 * volume)
    for s in range(n_samples):
        t = s / sample_rate
        buf.append(int(amplitude * math.sin(2 * math.pi * frequency * t)))
    return pygame.mixer.Sound(buffer=buf.tobytes())

def init_sounds():
    """Initialise Pygame mixer and simple tones."""
    global SOUND_ENABLED, HIT_PADDLE_SOUND, HIT_BRICK_SOUND, VICTORY_SOUND, GAME_OVER_SOUND
    try:
        pygame.mixer.init()
        SOUND_ENABLED = True
        HIT_PADDLE_SOUND = generate_tone(500)
        HIT_BRICK_SOUND = generate_tone(700)
        VICTORY_SOUND = generate_tone(880, 400)
        GAME_OVER_SOUND = generate_tone(220, 400)
    except Exception:
        SOUND_ENABLED = False
