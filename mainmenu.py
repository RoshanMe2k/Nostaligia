# main_menu.py
import pygame
import sys
from pong import play_pong
from snake import play_snake
from tetris import play_tetris
from space_invaders import play_space_invaders
from breakout import play_breakout
from racing_game import play_race
pygame.mixer.music.stop()
pygame.mixer.init()
music_custom = pygame.mixer.Sound("nostaliga_retro.wav")
music_custom.play()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
FONT_SIZE = 40

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, FONT_SIZE)
    menu_options = ["Pong (Bet u can't beat it)", "Tetris", "Snake", "Space Invaders", "BreakOut", "Road Racer" ,"Quit"]
    selected_option = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    return selected_option  # Return the selected option index

        screen.fill(BLACK)

        for i, option in enumerate(menu_options):
            color = WHITE if i == selected_option else (200, 200, 200)
            draw_text(screen, option, font, color, WIDTH // 2, HEIGHT // 2 + i * FONT_SIZE)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    while True:
        option = main_menu()

        if option == 0:
            play_pong()
        elif option == 1:
            play_tetris()
        elif option == 2:
            play_snake()
        elif option == 3:
            play_space_invaders()
        elif option == 4:
            play_breakout()
        elif option == 5:
            play_race()
        elif option == 5:
            pygame.quit()
            sys.exit()
