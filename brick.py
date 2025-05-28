import pygame
import config

class Brick:
    """Single brick that can be destroyed by the ball."""

    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, config.BRICK_WIDTH, config.BRICK_HEIGHT)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def on_destroy(self):
        pass  # Placeholder for sound or effects


def create_bricks():
    bricks = []
    start_x = (config.WIDTH - config.BRICK_COLS * config.BRICK_WIDTH) // 2
    start_y = 50
    for row in range(config.BRICK_ROWS):
        for col in range(config.BRICK_COLS):
            x = start_x + col * config.BRICK_WIDTH
            y = start_y + row * config.BRICK_HEIGHT
            color = config.ROW_COLORS[row % len(config.ROW_COLORS)]
            bricks.append(Brick(x, y, color))
    return bricks
