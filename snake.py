# snake.py
import pygame
import pygame.mixer
import sys
import random

pygame.mixer.init()

# Load the music file
pygame.mixer.music.load("snake.mp3")  # Replace with the actual path to your Snake music file

# Set the volume (optional)
pygame.mixer.music.set_volume(50)  # Adjust the volume as needed

# Start playing the music in a loop
pygame.mixer.music.play(-1)

# Constants
WIDTH, HEIGHT = 400, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE, BLACK, GREEN, RED = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Initial direction: right
        self.grow = False

    def move(self):
        current_head = self.body[0]
        new_head = (current_head[0] + self.direction[0], current_head[1] + self.direction[1])
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:]

    def check_boundary(self):
        head = self.body[0]
        return not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT)

    def draw(self, screen):
        screen.fill(BLACK)
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def play_snake():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food_position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.mixer.music.stop()  # Stop the music when quitting the game
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        snake.move()

        # Check for collision with food
        if snake.body[0] == food_position:
            snake.grow_snake()
            food_position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

        # Check for collision with boundaries or self
        if snake.check_collision() or snake.check_boundary():
            print("Game Over!")
            pygame.quit()
            sys.exit()

        snake.draw(screen)

        # Draw food
        pygame.draw.rect(screen, RED, (food_position[0] * GRID_SIZE, food_position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()
        clock.tick(10)  # Adjust the speed of the game

if __name__ == "__main__":
    play_snake()
