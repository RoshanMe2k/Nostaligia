import pygame
import sys
import random
import pygame.mixer

def play_race():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Load the music file
    pygame.mixer.music.load("race.mp3")  # Replace with the actual path to your Snake music file

    # Set the volume (optional)
    pygame.mixer.music.set_volume(50)  # Adjust the volume as needed

    # Start playing the music in a loop
    pygame.mixer.music.play(-1)

    # Set up the game window
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Road Racer")
    clock = pygame.time.Clock()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Road parameters
    road_width = 600
    road_border_width = 20
    road_color = (50, 50, 50)

    # Car parameters
    car_width = 50
    car_height = 80
    car_x = WIDTH // 2 - car_width // 2
    car_y = HEIGHT - car_height - 20
    car_speed = 5

    # Obstacle parameters
    obstacle_width = 50
    obstacle_height = 50
    obstacle_speed = 5

    # List to store obstacles
    obstacles = []

    # Function to draw the car
    def draw_car(x, y):
        pygame.draw.rect(screen, RED, (x, y, car_width, car_height))

    # Function to draw obstacles
    def draw_obstacles(obstacles):
        for obstacle in obstacles:
            pygame.draw.rect(screen, WHITE, obstacle)

    # Function to draw the road
    def draw_road():
        pygame.draw.rect(screen, road_color, (WIDTH // 2 - road_width // 2, 0, road_width, HEIGHT))
        pygame.draw.rect(screen, BLACK, (WIDTH // 2 - road_width // 2 - road_border_width, 0, road_border_width, HEIGHT))
        pygame.draw.rect(screen, BLACK, (WIDTH // 2 + road_width // 2, 0, road_border_width, HEIGHT))

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.mixer.music.stop()  # Stop the music when quitting the game
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > WIDTH // 2 - road_width // 2:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH // 2 + road_width // 2 - car_width:
            car_x += car_speed

        # Move obstacles
        for obstacle in obstacles:
            obstacle.y += obstacle_speed

        # Add a new obstacle
        if random.randint(0, 100) < 5:
            obstacle_x = random.randint(WIDTH // 2 - road_width // 2, WIDTH // 2 + road_width // 2 - obstacle_width)
            obstacle_y = -obstacle_height
            obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if pygame.Rect(car_x, car_y, car_width, car_height).colliderect(obstacle):
                print("Game Over!")
                pygame.quit()
                sys.exit()

        # Remove off-screen obstacles
        obstacles = [obstacle for obstacle in obstacles if obstacle.y < HEIGHT]

        # Draw everything on the screen
        screen.fill(BLACK)
        draw_road()
        draw_car(car_x, car_y)
        draw_obstacles(obstacles)

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)
if __name__ == "__main__":
    play_race()
