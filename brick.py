import pygame
import random
from config import WIDTH, BRICK_ROWS, BRICK_COLS, BRICK_WIDTH, BRICK_HEIGHT, ROW_COLORS
from powerup import PowerUp

class Brick:
    """Single brick"""
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def destroy(self):
        """Return a PowerUp instance with 20% probability."""
        if random.random() < 0.2:
            return PowerUp.random(self.rect.centerx, self.rect.centery)
        return None


def create_bricks():
    bricks = []
    start_x = (WIDTH - BRICK_COLS * BRICK_WIDTH) // 2
    start_y = 50
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = start_x + col * BRICK_WIDTH
            y = start_y + row * BRICK_HEIGHT
            color = ROW_COLORS[row]
            bricks.append(Brick(x, y, color))
    return bricks
