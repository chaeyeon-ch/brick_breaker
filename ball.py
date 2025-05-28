import pygame
import config

class Ball:
    """Ball that bounces around the screen."""

    def __init__(self, paddle):
        self.radius = config.BALL_RADIUS
        self.color = config.RED
        self.reset(paddle)

    def reset(self, paddle):
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top - 1
        self.vel = pygame.Vector2(0, 0)
        self.attached = True

    def launch(self):
        self.vel = pygame.Vector2(config.BALL_SPEED, -config.BALL_SPEED)
        self.attached = False

    def update(self, paddle, bricks):
        if self.attached:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top - 1
            return None

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

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
            paddle.on_hit()

        # Brick collisions
        hit_index = self.rect.collidelist(bricks)
        if hit_index != -1:
            brick = bricks.pop(hit_index)
            self.vel.y *= -1
            brick.on_destroy()
            return brick

        if self.rect.top > config.HEIGHT:
            return 'miss'

        return None

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
