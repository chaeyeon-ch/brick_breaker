import pygame
import config
from paddle import Paddle
from ball import Ball
from brick import Brick, create_bricks
from typing import List

class GameManager:
    """Manages game state, score, and drawing."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)
        self.state = "START"
        self.lives = 3
        self.score = 0
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks: List[Brick] = create_bricks()

    def reset(self):
        """Reset the entire game."""
        self.lives = 3
        self.score = 0
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = create_bricks()
        self.state = "START"

    def draw_text_center(self, text: str):
        surface = self.font.render(text, True, config.WHITE)
        rect = surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))
        self.screen.blit(surface, rect)

    def update(self):
        keys = pygame.key.get_pressed()

        if self.state == "START":
            self.paddle.update(keys)
            self.ball.update(self.paddle, self.bricks)
            if keys[pygame.K_SPACE]:
                self.ball.launch()
                self.state = "PLAYING"

        elif self.state == "PLAYING":
            self.paddle.update(keys)
            result = self.ball.update(self.paddle, self.bricks)
            if isinstance(result, Brick):
                self.score += 10
            elif result == "miss":
                self.lives -= 1
                if self.lives > 0:
                    self.ball.reset(self.paddle)
                else:
                    self.state = "GAME_OVER"
                    if config.SOUND_ENABLED and config.GAME_OVER_SOUND:
                        config.GAME_OVER_SOUND.play()
            if not self.bricks:
                self.state = "VICTORY"
                if config.SOUND_ENABLED and config.VICTORY_SOUND:
                    config.VICTORY_SOUND.play()

        elif self.state in ("GAME_OVER", "VICTORY"):
            if keys[pygame.K_r]:
                self.reset()

    def draw(self):
        self.screen.fill(config.BLACK)

        if self.state in ("START", "PLAYING", "GAME_OVER", "VICTORY"):
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)

        score_surf = self.font.render(f"Score: {self.score}", True, config.WHITE)
        lives_surf = self.font.render(f"Lives: {self.lives}", True, config.WHITE)
        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf, (config.WIDTH - lives_surf.get_width() - 10, 10))

        if self.state == "START":
            self.draw_text_center("Press SPACE to Start")
        elif self.state == "GAME_OVER":
            self.draw_text_center("Game Over - Press R to Restart")
        elif self.state == "VICTORY":
            self.draw_text_center("You Win! - Press R to Play Again")

        pygame.display.flip()
