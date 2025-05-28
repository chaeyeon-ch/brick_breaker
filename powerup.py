import pygame
import random
import config
from paddle import Paddle
from ball import Ball
from brick import Brick, create_bricks
from powerup import PowerUp

class GameManager:
    """Main game manager handling states and logic."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, config.FONT_SIZE)
        self.state = 'START'
        self.lives = 3
        self.score = 0
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = create_bricks()
        self.powerups = []  # 활성 파워업들
        self.paddle_normal_width = config.PADDLE_WIDTH  # 원래 패들 크기 저장

    def reset(self):
        self.lives = 3
        self.score = 0
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = create_bricks()
        self.powerups = []
        self.state = 'START'

    def apply_powerup(self, ptype):
        """파워업 효과 적용"""
        if ptype == 'expand':
            # 패들 크기 1.5배로 확장 (최대 200픽셀)
            new_width = min(200, int(self.paddle.rect.width * 1.5))
            old_center = self.paddle.rect.centerx
            self.paddle.rect.width = new_width
            self.paddle.rect.centerx = old_center
            # 화면 밖으로 나가지 않도록 조정
            if self.paddle.rect.left < 0:
                self.paddle.rect.left = 0
            elif self.paddle.rect.right > config.WIDTH:
                self.paddle.rect.right = config.WIDTH
        elif ptype == 'slow':
            # 공 속도 70%로 감소
            self.ball.vel *= 0.7
        elif ptype == 'multiball':
            # 현재는 점수만 추가 (나중에 실제 멀티볼 구현 가능)
            self.score += 50

    def draw_text_center(self, text):
        surface = self.font.render(text, True, config.WHITE)
        rect = surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))
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
            
            if isinstance(result, Brick):
                self.score += 10
                # 파워업 드롭 확률 체크 (30% 확률)
                if random.random() < 0.3:
                    powerup = PowerUp.random(result.rect.centerx, result.rect.centery)
                    self.powerups.append(powerup)
            elif result == 'miss':
                self.lives -= 1
                if self.lives > 0:
                    self.ball.reset(self.paddle)
                    self.state = 'START'  # Return to START state for next ball
                else:
                    self.state = 'GAME_OVER'
            
            # 파워업 업데이트
            for powerup in self.powerups[:]:  # 복사본으로 순회
                powerup.update()
                if powerup.rect.colliderect(self.paddle.rect):
                    self.apply_powerup(powerup.type)
                    self.powerups.remove(powerup)
                elif powerup.rect.top > config.HEIGHT:
                    self.powerups.remove(powerup)
            
            if not self.bricks:
                self.state = 'VICTORY'
        elif self.state in ('GAME_OVER', 'VICTORY'):
            if keys[pygame.K_r]:
                self.reset()

    def draw(self):
        self.screen.fill(config.BLACK)
        if self.state in ('START', 'PLAYING', 'GAME_OVER', 'VICTORY'):
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            
            # 파워업 그리기
            for powerup in self.powerups:
                powerup.draw(self.screen)

        score_surf = self.font.render(f"Score: {self.score}", True, config.WHITE)
        lives_surf = self.font.render(f"Lives: {self.lives}", True, config.WHITE)
        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf, (config.WIDTH - lives_surf.get_width() - 10, 10))

        if self.state == 'START':
            if self.lives == 3:
                self.draw_text_center("Press SPACE to Start")
            else:
                self.draw_text_center(f"Lives: {self.lives} - Press SPACE to Continue")
        elif self.state == 'GAME_OVER':
            self.draw_text_center("Game Over - Press R to Restart")
        elif self.state == 'VICTORY':
            self.draw_text_center("You Win! - Press R to Play Again")

        pygame.display.flip()
