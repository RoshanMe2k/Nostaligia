# tetris.py
import pygame.mixer
import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 400, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE, BLACK, CYAN, RED = (255, 255, 255), (0, 0, 0), (0, 255, 255), (255, 0, 0)

# Tetris class
class Tetris:
    def __init__(self):
        self.board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.spawn_piece()
        self.current_row, self.current_col = 0, GRID_WIDTH // 2
        self.game_over = False

    def spawn_piece(self):
        pieces = [
            [[1, 1, 1, 1]],  # I
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1], [1, 1]],  # O
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]]   # Z
        ]
        return random.choice(pieces)

    def rotate_piece(self):
        rotated_piece = [[self.current_piece[j][i] for j in range(len(self.current_piece))] for i in range(len(self.current_piece[0])-1, -1, -1)]
        if self.is_valid_move(rotated_piece, self.current_row, self.current_col):
            self.current_piece = rotated_piece

    def move_piece(self, row_offset, col_offset):
        if self.is_valid_move(self.current_piece, self.current_row + row_offset, self.current_col + col_offset):
            self.current_row += row_offset
            self.current_col += col_offset

    def is_valid_move(self, piece, row, col):
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j]:
                    if (row + i >= GRID_HEIGHT or col + j < 0 or col + j >= GRID_WIDTH or
                            (row + i < GRID_HEIGHT and self.board[row + i][col + j])):
                        return False
        return True
 

    def place_piece_on_board(self):
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[0])):
                if self.current_piece[i][j]:
                    self.board[self.current_row + i][self.current_col + j] = 1

    def clear_rows(self):
        full_rows = [row for row in range(GRID_HEIGHT) if all(self.board[row])]
        for row in full_rows:
            del self.board[row]
            self.board.insert(0, [0] * GRID_WIDTH)

    def check_collision(self):
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[0])):
                if self.current_piece[i][j] and (self.board[self.current_row + i][self.current_col + j] or self.current_row + i >= GRID_HEIGHT):
                    return True
        return False

    def draw(self, screen):
        screen.fill(BLACK)
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.board[i][j]:
                    pygame.draw.rect(screen, CYAN, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[0])):
                if self.current_piece[i][j]:
                    pygame.draw.rect(screen, CYAN, ((self.current_col + j) * GRID_SIZE, (self.current_row + i) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def play_tetris():
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


    tetris = Tetris()

    while not tetris.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.mixer.music.stop()  # Stop the music when quitting the game
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_piece(0, -1)
                elif event.key == pygame.K_RIGHT:
                    tetris.move_piece(0, 1)
                elif event.key == pygame.K_DOWN:
                    tetris.move_piece(1, 0)
                elif event.key == pygame.K_UP:
                    tetris.rotate_piece()

        if tetris.is_valid_move(tetris.current_piece, tetris.current_row + 1, tetris.current_col):
            tetris.move_piece(1, 0)
        else:
            tetris.place_piece_on_board()
            tetris.clear_rows()
            tetris.current_piece = tetris.spawn_piece()
            tetris.current_row, tetris.current_col = 0, GRID_WIDTH // 2
            if tetris.check_collision():
                tetris.game_over = True

        tetris.draw(screen)
        pygame.display.flip()
        clock.tick(5)  # Adjust the speed of the game

if __name__ == "__main__":
    play_tetris()
