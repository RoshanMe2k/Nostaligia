# pong.py

import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Paddle constants
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_SPEED = 10

# Ball constants
BALL_SIZE = 20
BALL_SPEED = 5
MAX_BALL_SPEED = 10

# Replace the Paddle class
# Replace the Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction):
        self.rect.y += direction * PADDLE_SPEED

        # Ensure the paddle stays within the screen boundaries
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def move_towards(self, target_y):
        if self.rect.centery < target_y:
            self.rect.y += PADDLE_SPEED
        elif self.rect.centery > target_y:
            self.rect.y -= PADDLE_SPEED

        # Ensure the paddle stays within the screen boundaries
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.direction = [1, 1]
        self.speed = BALL_SPEED

    def move(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Bounce off the top and bottom edges
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction[1] *= -1

    def check_collision(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.direction[0] *= -1
            self.speed = min(self.speed + 0.5, MAX_BALL_SPEED)

    def check_out_of_bounds(self):
        if self.rect.left < 0 or self.rect.right > WIDTH:
            return True
        return False

    def reset(self):
        self.rect.x = WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = HEIGHT // 2 - BALL_SIZE // 2
        self.speed = BALL_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

def display_score(screen, font, score_left, score_right):
    score_text = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))


def play_pong():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Game")
    clock = pygame.time.Clock()

    paddle_left = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle_right = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

    score_left, score_right = 0, 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Move the left paddle based on the ball's y-coordinate
        target_y = ball.rect.centery
        paddle_left.move_towards(target_y)

        # Move the right paddle manually
        if keys[pygame.K_UP]:
            paddle_right.move(-1)
        if keys[pygame.K_DOWN]:
            paddle_right.move(1)

        ball.move()
        ball.check_collision(paddle_left)
        ball.check_collision(paddle_right)

        if ball.check_out_of_bounds():
            if ball.rect.left < 0:
                score_right += 1
            else:
                score_left += 1
            ball.reset()

        screen.fill(BLACK)
        paddle_left.draw(screen)
        paddle_right.draw(screen)
        ball.draw(screen)
        display_score(screen, font, score_left, score_right)

        pygame.display.flip()
        clock.tick(60)
