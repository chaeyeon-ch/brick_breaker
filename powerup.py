import pygame
import random
import config

COLORS = {
    'expand': (0, 255, 0),      # 초록색 - 패들 확장
    'slow': (255, 255, 0),      # 노란색 - 공 속도 감소
    'multiball': (0, 255, 255)  # 청록색 - 멀티볼
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
        self.color = COLORS.get(ptype, config.WHITE)
        self.rect = pygame.Rect(x - self.SIZE//2, y - self.SIZE//2,
                                self.SIZE, self.SIZE)
        self.speed = 3  # 파워업 떨어지는 속도
        self.font = pygame.font.SysFont(None, 18)

    @classmethod
    def random(cls, x, y):
        """랜덤 파워업 생성"""
        ptype = random.choice(['expand', 'slow', 'multiball'])
        return cls(ptype, x, y)

    def update(self):
        """파워업을 아래로 이동"""
        self.rect.y += self.speed

    def draw(self, screen):
        """파워업을 화면에 그리기"""
        # 파워업 박스 그리기
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, config.BLACK, self.rect, 2)  # 테두리
        
        # 파워업 타입 문자 그리기
        label = self.font.render(LABELS[self.type], True, config.BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)
