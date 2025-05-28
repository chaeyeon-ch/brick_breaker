import pygame
import config

class Brick:
    """Single brick in the game."""

    def __init__(self, x: int, y: int, color):
        self.rect = pygame.Rect(x, y, config.BRICK_WIDTH, config.BRICK_HEIGHT)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


def create_bricks():
    """Create the initial set of bricks."""
    bricks = []
    start_x = (config.WIDTH - config.BRICK_COLS * config.BRICK_WIDTH) // 2
    start_y = 50
    for row in range(config.BRICK_ROWS):
        for col in range(config.BRICK_COLS):
            x = start_x + col * config.BRICK_WIDTH
            y = start_y + row * config.BRICK_HEIGHT
            color = config.ROW_COLORS[row]
            bricks.append(Brick(x, y, color))
    return bricks
