import pygame
import sys
import pygame.mixer
import random

pygame.init()
pygame.mixer.init()

spaceship_img = pygame.image.load("/spaceship.png")
alien_img = pygame.image.load("/alien.png")
bullet_img = pygame.image.load("/bullet.png")
def play_space_invaders():
    # Constants
    WIDTH, HEIGHT = 800, 600
    WHITE, BLACK = (255, 255, 255), (0, 0, 0)
    SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
    ALIEN_WIDTH, ALIEN_HEIGHT = 50, 50
    BULLET_WIDTH, BULLET_HEIGHT = 5, 15

    # Load the music file
    pygame.mixer.music.load("space_invaders.mp3")  # Replace with the actual path to your Snake music file

    # Set the volume (optional)
    pygame.mixer.music.set_volume(50)  # Adjust the volume as needed

    # Start playing the music in a loop
    pygame.mixer.music.play(-1)
    # Set up the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")

    # Game variables
    player_x = WIDTH // 2 - SPACESHIP_WIDTH // 2
    player_y = HEIGHT - SPACESHIP_HEIGHT - 10
    player_speed = 5

    alien_x = random.randint(0, WIDTH - ALIEN_WIDTH)  # Start the alien at a random horizontal position
    alien_y = -ALIEN_HEIGHT  # Start the alien above the screen
    alien_speed = 2

    bullet_x, bullet_y = 0, 0
    bullet_speed = 5
    bullet_state = "ready"  # "ready" means the bullet is ready to fire, "fire" means the bullet is currently moving

    score = 0
    font = pygame.font.Font(None, 36)
    losing_score = -3  # Adjust this value based on when you want the game to end

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.mixer.music.stop()  # Stop the music when quitting the game
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - SPACESHIP_WIDTH:
            player_x += player_speed

        # Shoot a bullet when the spacebar is pressed
        if keys[pygame.K_SPACE] and bullet_state == "ready":
            bullet_x = player_x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2
            bullet_y = player_y
            bullet_state = "fire"

        # Move the alien and deduct score if it reaches the bottom
        alien_y += alien_speed
        if alien_y > HEIGHT:
            alien_x = random.randint(0, WIDTH - ALIEN_WIDTH)
            alien_y = -ALIEN_HEIGHT
            score -= 1

        # Move the bullet
        if bullet_state == "fire":
            bullet_y -= bullet_speed
            if bullet_y <= 0:
                bullet_state = "ready"

        # Check for collisions
        if (
            alien_x < bullet_x < alien_x + ALIEN_WIDTH
            and alien_y < bullet_y < alien_y + ALIEN_HEIGHT
        ):
            bullet_state = "ready"
            alien_x = random.randint(0, WIDTH - ALIEN_WIDTH)
            alien_y = -ALIEN_HEIGHT
            score += 1

        # Draw everything on the screen
        screen.fill(BLACK)
        screen.blit(spaceship_img, (player_x, player_y))
        screen.blit(alien_img, (alien_x, alien_y))
        if bullet_state == "fire":
            screen.blit(bullet_img, (bullet_x, bullet_y))

        # Draw the score on the screen
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Check for losing condition
        if score <= losing_score:
            # Display "Game Over" and reset the game
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)  # Display "Game Over" for 2 seconds
            score = 0  # Reset the score
            alien_x = random.randint(0, WIDTH - ALIEN_WIDTH)
            alien_y = -ALIEN_HEIGHT

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        pygame.time.Clock().tick(60)
if __name__ == "__main__":
    play_space_invaders()
