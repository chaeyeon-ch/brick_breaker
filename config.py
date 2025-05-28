
# Game configuration constants
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

# Brick settings
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20


# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 7


# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 5


# UI
FONT_SIZE = 24
# 파워업 설정 (맨 아래에 추가)
POWERUP_SPEED = 3
POWERUP_DROP_CHANCE = 0.3  # 30% 확률로 파워업 드롭
