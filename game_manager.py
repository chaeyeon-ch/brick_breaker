import pygame
from config import WIDTH, HEIGHT, FPS, BLACK, WHITE
from paddle import Paddle
from ball import Ball
from brick import create_bricks, Brick
from powerup import PowerUp

class GameManager:
    """Handle game state, updates, and drawing"""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)
        self.reset()

    def reset(self):
        self.state = 'START'
        self.lives = 3
        self.score = 0
        self.paddle = Paddle()
        self.balls = [Ball(self.paddle)]
        self.bricks = create_bricks()
        self.powerups = []
        self.effects = {}

    def draw_text_center(self, text):
        surf = self.font.render(text, True, WHITE)
        rect = surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(surf, rect)

    def apply_powerup(self, pu):
        now = pygame.time.get_ticks()
        if pu.type == 'expand':
            self.paddle.expand()
            self.effects['expand'] = now + 10000
        elif pu.type == 'slow':
            for b in self.balls:
                b.set_speed(b.base_speed * 0.5)
            self.effects['slow'] = now + 10000
        elif pu.type == 'multiball':
            for angle in (-20, 20):
                nb = Ball(self.paddle)
                nb.launch()
                nb.rect.center = self.balls[0].rect.center
                nb.vel = nb.vel.rotate(angle)
                self.balls.append(nb)

    def update_effects(self):
        now = pygame.time.get_ticks()
        if 'expand' in self.effects and now > self.effects['expand']:
            self.paddle.reset_size()
            del self.effects['expand']
        if 'slow' in self.effects and now > self.effects['slow']:
            for b in self.balls:
                b.set_speed(b.base_speed)
            del self.effects['slow']

    def update(self):
        keys = pygame.key.get_pressed()
        if self.state == 'START':
            self.paddle.update(keys)
            if keys[pygame.K_SPACE]:
                self.balls[0].launch()
                self.state = 'PLAYING'
            self.balls[0].update(self.paddle, self.bricks)
        elif self.state == 'PLAYING':
            self.paddle.update(keys)
            for ball in self.balls[:]:
                result = ball.update(self.paddle, self.bricks)
                if isinstance(result, Brick):
                    self.score += 10
                    pu = result.destroy()
                    if pu:
                        self.powerups.append(pu)
                elif result == 'miss':
                    if len(self.balls) > 1:
                        self.balls.remove(ball)
                    else:
                        self.lives -= 1
                        if self.lives > 0:
                            self.balls = [Ball(self.paddle)]
                        else:
                            self.state = 'GAME_OVER'
            if not self.bricks:
                self.state = 'VICTORY'

            for pu in self.powerups[:]:
                pu.update()
                if pu.rect.top > HEIGHT:
                    self.powerups.remove(pu)
                elif pu.rect.colliderect(self.paddle.rect):
                    self.apply_powerup(pu)
                    self.powerups.remove(pu)

            self.update_effects()
        elif self.state in ('GAME_OVER', 'VICTORY'):
            if keys[pygame.K_r]:
                self.reset()

    def draw(self):
        self.screen.fill(BLACK)
        if self.state in ('START', 'PLAYING', 'GAME_OVER', 'VICTORY'):
            self.paddle.draw(self.screen)
            for ball in self.balls:
                ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            for pu in self.powerups:
                pu.draw(self.screen)

        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_surf = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf, (WIDTH - lives_surf.get_width() - 10, 10))

        if self.state == 'START':
            self.draw_text_center("Press SPACE to Start")
        elif self.state == 'GAME_OVER':
            self.draw_text_center("Game Over - Press R to Restart")
        elif self.state == 'VICTORY':
            self.draw_text_center("You Win! - Press R to Play Again")

        pygame.display.flip()
