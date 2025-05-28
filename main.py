import pygame
import sys
import math
from array import array

# Game constants
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

BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 7

BALL_RADIUS = 10
BALL_SPEED = 5

# Attempt to initialise mixer and generate simple tones
SOUND_ENABLED = False
HIT_PADDLE_SOUND = None
HIT_BRICK_SOUND = None
VICTORY_SOUND = None
GAME_OVER_SOUND = None

def generate_tone(frequency=440, duration_ms=150, volume=0.5):
    """Generate a sound tone using a sine wave."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = array('h')
    amplitude = int(32767 * volume)
    for s in range(n_samples):
        t = s / sample_rate
        buf.append(int(amplitude * math.sin(2 * math.pi * frequency * t)))
    return pygame.mixer.Sound(buffer=buf.tobytes())

try:
    pygame.mixer.init()
    SOUND_ENABLED = True
    HIT_PADDLE_SOUND = generate_tone(500)
    HIT_BRICK_SOUND = generate_tone(700)
    VICTORY_SOUND = generate_tone(880, 400)
    GAME_OVER_SOUND = generate_tone(220, 400)
except Exception:
    SOUND_ENABLED = False


class Paddle:
    """Player controlled paddle."""

    def __init__(self):
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

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    """Ball that bounces around the screen."""

    def __init__(self, paddle):
        self.radius = BALL_RADIUS
        self.color = RED
        self.reset(paddle)

    def reset(self, paddle):
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top - 1
        self.vel = pygame.Vector2(0, 0)
        self.attached = True

    def launch(self):
        self.vel = pygame.Vector2(BALL_SPEED, -BALL_SPEED)
        self.attached = False

    def update(self, paddle, bricks):
        if self.attached:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top - 1
            return None

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        # Missed paddle
        if self.rect.top > HEIGHT:
            return 'miss'

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
            # Change direction based on hit position
            offset = (self.rect.centerx - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
            self.vel.x = BALL_SPEED * offset
            if SOUND_ENABLED and HIT_PADDLE_SOUND:
                HIT_PADDLE_SOUND.play()

        # Brick collisions
        hit_index = self.rect.collidelist(bricks)
        if hit_index != -1:
            brick = bricks.pop(hit_index)
            self.vel.y *= -1
            if SOUND_ENABLED and HIT_BRICK_SOUND:
                HIT_BRICK_SOUND.play()
            return brick

        return None

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)


class Brick:
    """Single brick that can be destroyed by the ball."""

    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


def create_bricks():
    bricks = []
    start_x = (WIDTH - BRICK_COLS * BRICK_WIDTH) // 2
    start_y = 50
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = start_x + col * BRICK_WIDTH
            y = start_y + row * BRICK_HEIGHT
            bricks.append(pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT))
    return bricks


class GameManager:
    """Main game manager handling states and logic."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)
        self.state = 'START'
        self.lives = 3
        self.score = 0
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = create_bricks()

    def reset(self):
        self.lives = 3
        self.score = 0
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = create_bricks()
        self.state = 'START'

    def draw_text_center(self, text):
        surface = self.font.render(text, True, WHITE)
        rect = surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(surface, rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if self.state == 'START':
            self.paddle.update(keys)
            self.ball.update(self.paddle, self.bricks)
            if keys[pygame.K_SPACE]:
                self.ball.launch()
                self.state = 'PLAYING'
        elif self.state == 'PLAYING':
            self.paddle.update(keys)
            result = self.ball.update(self.paddle, self.bricks)
            if isinstance(result, pygame.Rect):
                self.score += 10
            elif result == 'miss':
                self.lives -= 1
                if self.lives > 0:
                    self.ball.reset(self.paddle)
                else:
                    self.state = 'GAME_OVER'
                    if SOUND_ENABLED and GAME_OVER_SOUND:
                        GAME_OVER_SOUND.play()
            if not self.bricks:
                self.state = 'VICTORY'
                if SOUND_ENABLED and VICTORY_SOUND:
                    VICTORY_SOUND.play()
        elif self.state in ('GAME_OVER', 'VICTORY'):
            if keys[pygame.K_r]:
                self.reset()

    def draw(self):
        self.screen.fill(BLACK)
        # Draw paddle and ball in all states except victory/game over when waiting
        if self.state in ('START', 'PLAYING', 'GAME_OVER', 'VICTORY'):
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick_rect in self.bricks:
                color = ROW_COLORS[(brick_rect.y - 50) // BRICK_HEIGHT]
                pygame.draw.rect(self.screen, color, brick_rect)

        # Score and lives
        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_surf = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf, (WIDTH - lives_surf.get_width() - 10, 10))

        # State messages
        if self.state == 'START':
            self.draw_text_center("Press SPACE to Start")
        elif self.state == 'GAME_OVER':
            self.draw_text_center("Game Over - Press R to Restart")
        elif self.state == 'VICTORY':
            self.draw_text_center("You Win! - Press R to Play Again")

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Brick Breaker AI Edition")
    clock = pygame.time.Clock()

    manager = GameManager(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        manager.update()
        manager.draw()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
