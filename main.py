
import sys
import pygame

from game_manager import GameManager
from config import WIDTH, HEIGHT, FPS


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
