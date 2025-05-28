import pygame
from config import WIDTH, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, WHITE

class Paddle:
    """Player controlled paddle"""
    def __init__(self):
        self.base_width = PADDLE_WIDTH
        self.rect = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2,
                                HEIGHT - PADDLE_HEIGHT * 2,
                                PADDLE_WIDTH,
                                PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()

    def expand(self):
        self.rect.width = int(self.base_width * 1.5)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def reset_size(self):
        self.rect.width = self.base_width

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
