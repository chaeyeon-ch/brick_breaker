import pygame
from config import WIDTH, HEIGHT, BALL_RADIUS, BALL_SPEED, RED

class Ball:
    """Ball that bounces around the screen"""
    def __init__(self, paddle):
        self.radius = BALL_RADIUS
        self.color = RED
        self.base_speed = BALL_SPEED
        self.reset(paddle)

    def reset(self, paddle):
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top - 1
        self.vel = pygame.Vector2(0, 0)
        self.attached = True

    def launch(self):
        self.vel = pygame.Vector2(self.base_speed, -self.base_speed)
        self.attached = False

    def set_speed(self, speed):
        if self.vel.length() != 0:
            direction = self.vel.normalize()
            self.vel = direction * speed

    def update(self, paddle, bricks):
        if self.attached:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top - 1
            return None

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        # Wall collisions
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vel.x *= -1
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        if self.rect.top <= 0:
            self.vel.y *= -1
            self.rect.top = 0

        # Paddle collision
        if self.rect.colliderect(paddle.rect) and self.vel.y > 0:
            self.rect.bottom = paddle.rect.top - 1
            self.vel.y *= -1
            offset = (self.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
            self.vel.x = self.base_speed * offset

        # Brick collisions
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                bricks.remove(brick)
                self.vel.y *= -1
                return brick

        # Bottom of screen
        if self.rect.top > HEIGHT:
            return 'miss'
        return None

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
