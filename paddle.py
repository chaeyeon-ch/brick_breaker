import pygame
import config

class Paddle:
    """Player controlled paddle."""

    def __init__(self):
        self.rect = pygame.Rect(
            (config.WIDTH - config.PADDLE_WIDTH) // 2,
            config.HEIGHT - config.PADDLE_HEIGHT * 2,
            config.PADDLE_WIDTH,
            config.PADDLE_HEIGHT,
        )
        self.speed = config.PADDLE_SPEED
    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > config.WIDTH:
            self.rect.right = config.WIDTH

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()


    def draw(self, surface):
        pygame.draw.rect(surface, config.WHITE, self.rect)

    def on_hit(self):
        pass  # Placeholder for hit sound
