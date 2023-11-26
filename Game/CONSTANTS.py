from Vector import Vector2D

SCREEN_SIZE = (500, 500)
BACKGROUND_IMAGE = 'assets/background.png'
UP_SPRITE = 'assets/flappy_bird_up.png'
PIPE_SPRITE = 'assets/pipe_sprite.png'
BIRD_HEIGHT = 50
BIRD_WIDTH = 50
GRAVITY = Vector2D(0, 1000)
CLAMPED_ACCELERATION = Vector2D(0, 1800)
BIRD_START = (50, 50)
JUMP_COOLDOWN = 60 * 7.5
JUMP_DURATION = (66 + 2/3)
JUMP_ACCELERATION = Vector2D(0, -16000)
SPEED_MULTIPLIER = 1
GEN_SIZE = 60
