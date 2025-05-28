import pygame
import sys
import config
from game_manager import GameManager


def main():
    pygame.init()
    config.init_sounds()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
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
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
