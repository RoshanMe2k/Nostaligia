# breakout.py
import pygame.mixer
import pygame
import sys
import random

def play_breakout():
    # Constants
    WIDTH, HEIGHT = 800, 600
    WHITE, BLACK = (255, 255, 255), (0, 0, 0)
    PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
    BALL_RADIUS = 10
    BRICK_WIDTH, BRICK_HEIGHT = 60, 20
    BRICK_ROWS, BRICK_COLS = 5, 10

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Load the music file
    pygame.mixer.music.load("breakout.mp3")  # Replace with the actual path to your Snake music file

    # Set the volume (optional)
    pygame.mixer.music.set_volume(50)  # Adjust the volume as needed

    # Start playing the music in a loop
    pygame.mixer.music.play(-1)
    # Set up the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout")

    # Function to generate a random color
    def generate_random_color():
        return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

    # Game variables
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    paddle_y = HEIGHT - PADDLE_HEIGHT - 10
    paddle_speed = 8

    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_speed_x, ball_speed_y = 5, -5  # Change the initial direction

    bricks = []

    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick_color = generate_random_color()
            brick = pygame.Rect(
                col * BRICK_WIDTH + (WIDTH - BRICK_WIDTH * BRICK_COLS) // 2,
                row * BRICK_HEIGHT + 50,
                BRICK_WIDTH,
                BRICK_HEIGHT,
            )
            bricks.append((brick, brick_color))

    # Flag to track game state
    game_over = False
    win = False

    # Main game loop
    while not game_over and not win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.mixer.music.stop()  # Stop the music when quitting the game
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Bounce off walls
        if ball_x <= 0 or ball_x >= WIDTH:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # Bounce off the paddle
        if (
            paddle_x < ball_x < paddle_x + PADDLE_WIDTH
            and paddle_y < ball_y < paddle_y + PADDLE_HEIGHT
        ):
            ball_speed_y = -ball_speed_y

        # Check for collisions with bricks
        for brick, color in bricks:
            if brick.colliderect(pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)):
                ball_speed_y = -ball_speed_y
                bricks.remove((brick, color))
                break

        # Draw everything on the screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        # Check for win condition
        if not bricks:
            win = True

        # Check for game over condition
        if ball_y > HEIGHT:
            game_over = True

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        pygame.time.Clock().tick(60)

    # Display win or game over screen
    font = pygame.font.Font(None, 72)
    if win:
        text = font.render("You Win!", True, WHITE)
    else:
        text = font.render("Game Over", True, WHITE)

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Wait for a few seconds before exiting
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    play_breakout()