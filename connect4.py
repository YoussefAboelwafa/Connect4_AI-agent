import pygame
import sys
import os
import random  
import Engine
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
DARK_BLUE=(0,46,177)
class ConnectFour:
    def __init__(self):
        self.board=[[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
        pygame.init()

        WINDOW_SIZE = (COLUMN_COUNT * SQUARE_SIZE, ROW_COUNT * SQUARE_SIZE)
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Connect 4")
        self.animation_frames = []
        for i in range(1, 30): 
            frame_path = os.path.join("frames", f"frame{i}.png")
            self.animation_frames.append(pygame.transform.scale(pygame.image.load(frame_path), WINDOW_SIZE))
        self.clock = pygame.time.Clock()
        self.frame_index = 0
        self.menu=True
        self.main_menu()

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
    
    def is_valid_location(self, col):
        return self.board[0][col] == 0
    
    def get_next_open_row(self, col):
        for r in range(ROW_COUNT - 1, -1, -1):
            if self.board[r][col] == 0:
                return r
    
    def draw_board(self, current_player):
        print(self.board)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, DARK_BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                color = WHITE
                if self.board[r][c] == 1:
                    color = RED
                elif self.board[r][c] == 2:
                    color = YELLOW
                pygame.draw.circle(self.screen, color, (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2), 45)

        # Draw the current player's piece above the selected column
        if current_player == 1:
            color = RED
        else:
            color = YELLOW

        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_column = mouse_x // SQUARE_SIZE

        pygame.draw.circle(self.screen, color, (selected_column * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 2), 45)

        pygame.display.update()
                
    def winning_move(self, piece):
        # Check horizontal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    return True

        # Check vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    return True

        # Check positive slope diagonal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        # Check negative slope diagonal
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

        return False
    
    def ai_move(self):
        return Engine.agent(self.board,4)
    
    def display_menu(self):
        font = pygame.font.SysFont("monospace", 30,True)
        title = "Welcome To Our Connect 4 Game"
        title_text = font.render(title, True, BLACK)
        player_vs_player_text = font.render("Player vs. Player", True, BLACK)
        player_vs_ai_text = font.render("Player vs. AI", True, BLACK)
        quit_text = font.render("Quit", True, BLACK)
        self.screen.blit(player_vs_player_text, (200, 250))
        self.screen.blit(player_vs_ai_text, (230, 300))
        self.screen.blit(title_text, (80, 150))
        self.screen.blit(quit_text, (315, 350))
        pygame.display.update()

    def main_menu(self):
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] > 250 and event.pos[1] < 300:
                        self.player_vs_player = True
                        self.menu = False
                    elif event.pos[1] > 300 and event.pos[1] < 350:
                        self.player_vs_player = False
                        self.menu = False
                    elif event.pos[1]>350 and event.pos[1] <400:
                        pygame.quit()
                        sys.exit()
            self.screen.fill(BLACK)
            self.screen.blit(self.animation_frames[self.frame_index],(0,0))
            self.clock.tick(10)
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.display_menu()

    def show_winner_popup(self,player):
        font = pygame.font.SysFont("monospace", 60, True)
        if self.player_vs_player:
            pygame.display.set_caption(f"Player {player} wins!")
            win_text = font.render(f"Player {player} wins!", True, GREEN if player == 1 else GREEN)
            self.screen.blit(win_text, (80, ROW_COUNT * SQUARE_SIZE // 2))
            
        else:
            win_text = font.render(f"AI wins!", True, GREEN)
            if player=='AI':
                pygame.display.set_caption('Computer Wins')
                win_text = font.render(f"Computer wins!", True, GREEN if player == 1 else GREEN)

            else:
                pygame.display.set_caption('You Win')
                win_text = font.render(f"You win!", True, GREEN if player == 1 else GREEN)
            self.screen.blit(win_text, (80, ROW_COUNT * SQUARE_SIZE // 2))
        font = pygame.font.SysFont("monospace", 30, True)
        fin_text=font.render("Main menu press x, Quit press esc ", True, GREEN if player == 1 else GREEN)
        self.screen.blit(fin_text, (80, ROW_COUNT * SQUARE_SIZE // 2+100))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    self.menu = True
                    self.board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                    self.main_menu()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def main(self):
        turn=0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player_vs_player:
                        col = event.pos[0] // SQUARE_SIZE
                        if self.is_valid_location(col):
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, turn + 1)
                            self.screen.fill(WHITE)
                            self.draw_board(turn + 1)
                            if self.winning_move(turn + 1):
                                self.show_winner_popup(turn+1)
                            turn = 1 - turn
                            continue
                    else:
                        if not self.menu:
                            col = event.pos[0] // SQUARE_SIZE
                            if self.is_valid_location(col):
                                row = self.get_next_open_row(col)
                                self.drop_piece(row, col, turn + 1)
                                self.screen.fill(WHITE)
                                self.draw_board(turn + 1)
                                if self.winning_move(turn + 1):
                                    self.show_winner_popup(turn+1)
                                turn = 1 - turn
                                continue
                elif not self.player_vs_player and turn == 1:
                    if not self.menu:
                        ai_col = self.ai_move()
                        ai_row = self.get_next_open_row(ai_col)
                        self.drop_piece(ai_row, ai_col, 2)
                        self.screen.fill(WHITE)
                        self.draw_board(turn)
                        if self.winning_move(2):
                            self.show_winner_popup("AI")
                        turn = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        self.menu = True
                        self.board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                        turn = 0
                        self.main_menu()
            self.screen.fill(WHITE)
            self.draw_board(turn+1)
            pygame.display.update()

if __name__ == "__main__":
    game = ConnectFour()
    game.main()

       