# tetris.py
import pygame.mixer
import pygame
import sys
import random
import pygame
import random

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

# Tetris pieces
PIECES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
]

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Scoring
score = 0

def create_board():
    return [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

def draw_board(board):
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col]:
                pygame.draw.rect(screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

def draw_piece(piece, row, col):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j]:
                pygame.draw.rect(screen, RED, ((col + j) * GRID_SIZE, (row + i) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BLACK, ((col + j) * GRID_SIZE, (row + i) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

def is_valid_move(board, piece, row, col):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if (
                piece[i][j]
                and (
                    row + i >= BOARD_HEIGHT
                    or col + j < 0
                    or col + j >= BOARD_WIDTH
                    or row + i < 0
                    or board[row + i][col + j]
                )
            ):
                return False
    return True

def rotate_piece(piece):
    return [list(row[::-1]) for row in zip(*piece)]

def merge_piece(board, piece, row, col):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j]:
                board[row + i][col + j] = 1

def clear_rows(board):
    global score
    full_rows = [i for i, row in enumerate(board) if all(row)]
    for row in full_rows:
        del board[row]
        board.insert(0, [0] * BOARD_WIDTH)
        score += 100  # Award points for each cleared row

def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def play_tetris():
    global score
    clock = pygame.time.Clock()
    board = create_board()
    current_piece = random.choice(PIECES)
    current_row, current_col = 0, BOARD_WIDTH // 2
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris Game")
    clock = pygame.time.Clock()
    pygame.mixer.init()

    # Load the music file
    pygame.mixer.music.load("tetris.mp3")  # Replace with the actual path to your Snake music file

    # Set the volume (optional)
    pygame.mixer.music.set_volume(50)  # Adjust the volume as needed

    # Start playing the music in a loop
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.mixer.music.stop()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and is_valid_move(board, current_piece, current_row, current_col - 1):
                    current_col -= 1
                elif event.key == pygame.K_RIGHT and is_valid_move(board, current_piece, current_row, current_col + 1):
                    current_col += 1
                elif event.key == pygame.K_DOWN and is_valid_move(board, current_piece, current_row + 1, current_col):
                    current_row += 1
                elif event.key == pygame.K_SPACE:
                    rotated_piece = rotate_piece(current_piece)
                    if is_valid_move(board, rotated_piece, current_row, current_col):
                        current_piece = rotated_piece

        if not is_valid_move(board, current_piece, current_row + 1, current_col):
            merge_piece(board, current_piece, current_row, current_col)
            clear_rows(board)
            current_row, current_col = 0, BOARD_WIDTH // 2
            current_piece = random.choice(PIECES)

        elif is_valid_move(board, current_piece, current_row + 1, current_col):
            current_row += 1

        screen.fill(BLACK)
        draw_board(board)
        draw_piece(current_piece, current_row, current_col)
        display_score()

        pygame.display.flip()
        clock.tick(5)

if __name__ == "__main__":
    play_tetris()
