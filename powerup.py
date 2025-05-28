import pygame
import random
from config import POWERUP_SPEED, WHITE, BLACK

COLORS = {
    'expand': (0, 255, 0),
    'slow': (255, 255, 0),
    'multiball': (0, 255, 255)
}

LABELS = {
    'expand': 'E',
    'slow': 'S',
    'multiball': 'M'
}

class PowerUp:
    """Falling power-up box"""
    SIZE = 20
    def __init__(self, ptype, x, y):
        self.type = ptype
        self.color = COLORS.get(ptype, WHITE)
        self.rect = pygame.Rect(x - self.SIZE//2, y - self.SIZE//2,
                                self.SIZE, self.SIZE)
        self.speed = POWERUP_SPEED
        self.font = pygame.font.SysFont(None, 18)

    @classmethod
    def random(cls, x, y):
        ptype = random.choice(['expand', 'slow', 'multiball'])
        return cls(ptype, x, y)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        label = self.font.render(LABELS[self.type], True, BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)
