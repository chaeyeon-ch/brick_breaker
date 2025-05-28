import pygame
import config
from typing import List, Optional
from brick import Brick
from paddle import Paddle

class Ball:
    """Ball that moves and collides with game objects."""

    def __init__(self, paddle: Paddle):
        self.radius = config.BALL_RADIUS
        self.color = config.RED
        self.reset(paddle)

    def reset(self, paddle: Paddle):
        """Attach the ball to the paddle."""
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top - 1
        self.vel = pygame.Vector2(0, 0)
        self.attached = True

    def launch(self):
        """Launch the ball from the paddle."""
        self.vel = pygame.Vector2(config.BALL_SPEED, -config.BALL_SPEED)
        self.attached = False

    def update(self, paddle: Paddle, bricks: List[Brick]) -> Optional[Brick | str]:
        """Move the ball and handle collisions."""
        if self.attached:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top - 1
            return None

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        # Early check for falling below the screen
        if self.rect.top > config.HEIGHT:
            return "miss"

        # Wall collisions
        if self.rect.left <= 0 or self.rect.right >= config.WIDTH:
            self.vel.x *= -1
            self.rect.clamp_ip(pygame.Rect(0, 0, config.WIDTH, config.HEIGHT))
        if self.rect.top <= 0:
            self.vel.y *= -1
            self.rect.top = 0

        # Paddle collision
        if self.rect.colliderect(paddle.rect) and self.vel.y > 0:
            self.rect.bottom = paddle.rect.top - 1
            self.vel.y *= -1
            offset = (self.rect.centerx - paddle.rect.centerx) / (config.PADDLE_WIDTH / 2)
            self.vel.x = config.BALL_SPEED * offset
            if config.SOUND_ENABLED and config.HIT_PADDLE_SOUND:
                config.HIT_PADDLE_SOUND.play()

        # Brick collision
        index = self.rect.collidelist([b.rect for b in bricks])
        if index != -1:
            brick = bricks.pop(index)
            self.vel.y *= -1
            if config.SOUND_ENABLED and config.HIT_BRICK_SOUND:
                config.HIT_BRICK_SOUND.play()
            return brick

        return None

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
