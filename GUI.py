import pygame
import sys
import os
import random
import engine
from TreeVisualise import TreeNode

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 46, 177)
LIGHT_GRAY = (200, 200, 200)
GRAY = (128, 128, 128)


def convert_state_to_tree(tree):
    state = list(tree.keys())[0]
    root = TreeNode(engine.convert_from_string_to_grid(state), tree[state]["value"])
    childs = tree[state]["childs"]
    if len(childs) == 0:
        return root
    for child in childs:
        root.add_child(convert_state_to_tree(child))
    return root


class ConnectFour:
    def __init__(self):
        self.board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
        pygame.init()

        WINDOW_SIZE = ((COLUMN_COUNT + 3) * SQUARE_SIZE, (ROW_COUNT + 1) * SQUARE_SIZE)
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        # ROW_COUNT=self.screen.get_height()
        # COLUMN_COUNT=self.screen.get_width()
        pygame.display.set_caption("Connect 4")
        self.animation_frames = []
        for i in range(1, 30):
            frame_path = os.path.join("frames", f"frame{i}.png")
            self.animation_frames.append(
                pygame.transform.scale(pygame.image.load(frame_path), WINDOW_SIZE)
            )
        self.clock = pygame.time.Clock()
        self.frame_index = 0
        self.menu = True
        self.main_menu()
        self.main()

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def resize_game_window(self, width, height, player):
        SQUARE_SIZE = min(width // COLUMN_COUNT, height // ROW_COUNT)
        self.screen = pygame.display.set_mode(
            (COLUMN_COUNT * SQUARE_SIZE, ROW_COUNT * SQUARE_SIZE), pygame.RESIZABLE
        )
        self.animation_frames = [
            pygame.transform.scale(
                frame, (COLUMN_COUNT * SQUARE_SIZE, ROW_COUNT * SQUARE_SIZE)
            )
            for frame in self.animation_frames
        ]
        if player != -1:
            self.draw_board(player)

    def is_valid_location(self, col):
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT - 1, -1, -1):
            if self.board[r][col] == 0:
                return r

    def draw_board(self, current_player):
        for c in range(COLUMN_COUNT):
            for r in range(1, ROW_COUNT + 1):
                pygame.draw.rect(
                    self.screen,
                    DARK_BLUE,
                    (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )
                color = BLACK
                if self.board[r - 1][c] == 1:
                    color = RED
                elif self.board[r - 1][c] == 2:
                    color = YELLOW
                pygame.draw.circle(
                    self.screen,
                    color,
                    (
                        c * SQUARE_SIZE + SQUARE_SIZE // 2,
                        r * SQUARE_SIZE + SQUARE_SIZE // 2,
                    ),
                    45,
                )

        # Draw the current player's piece above the selected column
        if current_player == 1:
            color = RED
        else:
            color = YELLOW

        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_column = mouse_x // SQUARE_SIZE
        for i in range(COLUMN_COUNT, COLUMN_COUNT + 3):
            for j in range(ROW_COUNT + 1):
                pygame.draw.rect(
                    self.screen,
                    LIGHT_GRAY,
                    (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )
        if selected_column < 7 and self.is_valid_location(selected_column):
            pygame.draw.circle(
                self.screen,
                color,
                (selected_column * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 2),
                45,
            )

        if not self.player_vs_player:
            # Draw the solve tree button
            solve_tree_button = pygame.Rect(
                (COLUMN_COUNT) * SQUARE_SIZE + 50,
                4 * SQUARE_SIZE,
                2 * SQUARE_SIZE,
                SQUARE_SIZE,
            )
            font = pygame.font.Font(None, 30)
            text = font.render("Solve Tree", True, BLACK)
            self.screen.blit(
                text,
                (
                    solve_tree_button.x
                    + solve_tree_button.width // 2
                    - text.get_width() // 2,
                    solve_tree_button.y
                    + solve_tree_button.height // 2
                    - text.get_height() // 2,
                ),
            )
            pygame.draw.rect(self.screen, GRAY, solve_tree_button, 2)

            # Check if the solve tree button has been clicked
            if pygame.mouse.get_pressed()[0]:
                if solve_tree_button.collidepoint(mouse_x, mouse_y):
                    try:
                        self.visualize_solve_tree()
                    except:
                        pass
        # Draw the properties panel
        self.draw_properties(current_player)
        # pygame.display.update()

    def visualize_solve_tree(self):
        self.screen.fill(WHITE)
        pygame.display.flip()
        root = convert_state_to_tree(self.tree)
        root_x = 400
        root_y = 100

        backIconAccent = pygame.image.load("images/back-icon.png").convert_alpha()
        backIcon = pygame.image.load("images/back-icon-accent.png").convert_alpha()
        backIcon = pygame.transform.scale(backIcon, (50, 50))
        backIconAccent = pygame.transform.scale(backIconAccent, (50, 50))
        font = pygame.font.SysFont("monospace", 30, True)
        node_expanded_text = font.render(
            f"Nodes expanded {self.node_expanded}", True, BLACK
        )
        self.screen.blit(node_expanded_text, (20, 100))
        backIconRect = backIcon.get_rect()
        backIconRect.x = 0
        backIconRect.y = 0
        backIconRectAccent = backIconAccent.get_rect()
        backIconRectAccent.x = 0
        backIconRectAccent.y = 0
        backIconRectAccent.center = backIconRect.center
        backIconRect.center = backIconRect.center
        self.screen.blit(backIcon, backIconRect)
        self.screen.blit(backIconAccent, backIconRectAccent)
        undo_level_botton = pygame.image.load("images/undo.png").convert_alpha()
        undo_level_botton = pygame.transform.scale(undo_level_botton, (50, 50))
        undo_level_botton_rect = undo_level_botton.get_rect()
        undo_level_botton_rect.x = (COLUMN_COUNT + 3) * SQUARE_SIZE - 50
        undo_level_botton_rect.y = 50
        undo_level_botton_rect.center = ((COLUMN_COUNT + 3) * SQUARE_SIZE - 50, 50)
        # self.screen.blit(undo_level_botton, undo_level_botton_rect)
        first_child_x = root_x - 385
        first_child_y = root_y + 300
        child_offset = 140
        root1 = root
        his = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if backIconRect.collidepoint(event.pos):
                        self.screen.fill(WHITE)
                        return
                    elif undo_level_botton_rect.collidepoint(event.pos):
                        if his:
                            self.screen.fill(WHITE)
                            self.screen.blit(backIcon, backIconRect)
                            self.screen.blit(backIconAccent, backIconRectAccent)
                            self.screen.blit(undo_level_botton, undo_level_botton_rect)
                            self.screen.blit(node_expanded_text, (20, 100))
                            root1 = his[-1]
                            his.pop()
                    else:
                        child_index = 0
                        self.screen.fill(WHITE)
                        self.screen.blit(backIcon, backIconRect)
                        self.screen.blit(backIconAccent, backIconRectAccent)
                        self.screen.blit(undo_level_botton, undo_level_botton_rect)
                        for child in root1.children:
                            if (
                                first_child_x + child_offset * child_index
                                <= event.pos[0]
                                <= first_child_x + child_offset * child_index + 100
                                and first_child_y <= event.pos[1] <= first_child_y + 100
                            ):
                                if len(child.children) > 1:
                                    his.append(root1)
                                    root1 = child
                                    # for i in child.children:
                                    #     print (i.value)
                                break
                            child_index += 1

            self.draw_tree(root1, root_x, root_y)
            pygame.display.update()

    # draw the first level of children for the root
    def draw_tree(self, node, x, y):
        if node is None:
            return
        # Draw the current board state
        self.draw_mini_board(node.board, 25, x, y)
        # Draw the current node's value
        font = pygame.font.Font(None, 30)
        text = font.render(str(node.value), True, BLACK)
        self.screen.blit(text, (x + 200, y + 50))

        # Draw lines to children
        child_x = x - 385  # Adjust as needed
        child_y = y + 300  # Adjust as needed

        for child in node.children:
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (x + 180 // 2, y + 150),
                (child_x + 100 // 2, child_y),
                2,
            )
            self.draw_mini_board(child.get_board(), 18, child_x, child_y)
            text = font.render(str(child.value), True, BLACK)
            self.screen.blit(text, (child_x + 10, child_y + 120))
            child_x += 140  # Adjust as needed

    def draw_mini_board(self, state, size, x, y):
        MINISQUARESIZE = size
        MINI_PIECE_RADIUS = MINISQUARESIZE / 2 - 2
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                col = x + c * MINISQUARESIZE
                row = y + r * MINISQUARESIZE
                piece = state[r][c]
                pygame.draw.rect(
                    self.screen, GRAY, (col, row, MINISQUARESIZE, MINISQUARESIZE)
                )
                if piece == 1:
                    pygame.draw.circle(
                        self.screen,
                        RED,
                        (col + MINISQUARESIZE // 2, row + MINISQUARESIZE // 2),
                        MINI_PIECE_RADIUS,
                    )
                elif piece == 2:
                    pygame.draw.circle(
                        self.screen,
                        YELLOW,
                        (col + MINISQUARESIZE // 2, row + MINISQUARESIZE // 2),
                        MINI_PIECE_RADIUS,
                    )
                elif piece == 0:
                    pygame.draw.circle(
                        self.screen,
                        WHITE,
                        (int(col + MINISQUARESIZE / 2), int(row + MINISQUARESIZE / 2)),
                        MINI_PIECE_RADIUS,
                    )
        pygame.display.update()

    def check_is_winning_move(self, piece, col, row):
        count = 0

        def check_direction(dc, dr):
            nonlocal count
            for c in range(COLUMN_COUNT - 3):
                for r in range(ROW_COUNT - 3) if dr != -1 else range(3, ROW_COUNT):
                    if all(
                        self.board[r + i * dr][c + i * dc] == piece for i in range(4)
                    ):
                        count += (
                            1
                            if any(
                                c + i * dc == col and r + i * dr == row
                                for i in range(4)
                            )
                            else 0
                        )

        # Check horizontal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    count += (
                        1 if any(c + i == col and r == row for i in range(4)) else 0
                    )

        # Check vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    count += (
                        1 if any(c == col and r + i == row for i in range(4)) else 0
                    )

        # Check positive slope diagonal
        check_direction(1, 1)

        # Check negative slope diagonal
        check_direction(1, -1)

        return count

    def ai_move(self):
        if self.selected_ai_engine == "Minimax":
            choise, self.tree, self.node_expanded = engine.agent(
                self.board, self.difficulty, 1
            )
            return choise
        else:
            choise, self.tree, self.node_expanded = engine.agent(
                self.board, self.difficulty, 2
            )
            return choise

    def ai_menu(self):
        ai_menu = True
        selected_ai_engine = "Minimax"  # Default AI engine
        ai_difficulty = 1  # Default difficulty level
        difficulty_change_delay = 3
        frame_counter = 0
        while ai_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 300 <= event.pos[1] <= 350:
                        selected_ai_engine = "Minimax"
                        ai_menu = False
                    elif 350 <= event.pos[1] <= 400:
                        selected_ai_engine = (
                            "pruning"  # Adjust for your actual AI engine
                        )
                        ai_menu = False

            self.screen.fill(BLACK)
            self.screen.blit(self.animation_frames[self.frame_index], (0, 0))
            self.clock.tick(10)
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)

            font = pygame.font.SysFont("monospace", 30, True)
            menu_rect = pygame.Surface((600, 400), pygame.SRCALPHA)
            pygame.draw.rect(
                menu_rect, (255, 255, 255, 128), (0, 0, 550, 300), border_radius=10
            )
            self.screen.blit(menu_rect, (230, 210))
            title_text = font.render("Choose AI Engine:", True, BLACK)
            title_text_3d_left = font.render("Choose AI Engine:", True, BLACK)
            title_text_3d_left_pos = (240 - 1, 255 + 1)
            self.screen.blit(title_text, (240, 255))
            self.screen.blit(title_text_3d_left, title_text_3d_left_pos)

            option_text = font.render("MiniMax 'without pruning'", True, BLACK)
            option_text_3d_left = font.render("MiniMax 'without pruning'", True, BLACK)
            option_text_3d_left_pos = (300 - 1, 300 + 1)
            self.screen.blit(option_text, (300, 300))
            self.screen.blit(option_text_3d_left, option_text_3d_left_pos)

            option_text = font.render(
                "Minimax 'with pruning' ", True, BLACK
            )  # Adjust for your actual AI engine
            option_text_3d_left = font.render("Minimax 'with pruning'", True, BLACK)
            option_text_3d_left_pos = (300 - 1, 350 + 1)
            self.screen.blit(option_text, (300, 350))
            self.screen.blit(option_text_3d_left, option_text_3d_left_pos)

            difficulty_text = font.render(
                f"Difficulty: {ai_difficulty}", True, DARK_BLUE
            )
            difficulty_text_3d_left = font.render(
                f"Difficulty: {ai_difficulty}", True, DARK_BLUE
            )
            difficulty_text_3d_left_pos = (350 - 1, 400 + 1)
            self.screen.blit(difficulty_text, (350, 400))
            self.screen.blit(difficulty_text_3d_left, difficulty_text_3d_left_pos)

            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and frame_counter == 0:
                ai_difficulty += 1
                frame_counter = difficulty_change_delay
            elif keys[pygame.K_DOWN] and ai_difficulty > 1 and frame_counter == 0:
                ai_difficulty -= 1
                frame_counter = difficulty_change_delay

            frame_counter = max(0, frame_counter - 1)

        return selected_ai_engine, ai_difficulty

    def display_menu(self):
        font = pygame.font.SysFont("monospace", 30, True)
        title = "Welcome To Our Connect 4 Game"
        title_text = font.render(title, True, BLACK)
        title_text_3d_left = font.render(title, True, BLACK)
        title_text_3d_right = font.render(title, True, BLACK)
        title_text_3d_left_pos = (240 - 1, 225 + 1)
        menu_rect = pygame.Surface((600, 400), pygame.SRCALPHA)
        pygame.draw.rect(
            menu_rect, (255, 255, 255, 128), (0, 0, 550, 300), border_radius=10
        )
        self.screen.blit(menu_rect, (230, 210))
        player_vs_player_text = font.render("Player vs. Player", True, BLACK)
        player_vs_ai_text = font.render("Player vs. AI", True, BLACK)
        quit_text = font.render("Quit", True, BLACK)
        player_vs_player_text_3d_left = font.render("Player vs. Player", True, BLACK)
        player_vs_ai_text_3d_left = font.render("Player vs. AI", True, BLACK)
        quit_text_3d_left = font.render("Quit", True, BLACK)
        player_vs_player_text_3d_left_pos = (350 - 1, 300 + 1)
        player_vs_ai_text_3d_left_pos = (390 - 1, 350 + 1)
        quit_text_3d_left_pos = (460 - 1, 400 + 1)
        self.screen.blit(title_text_3d_left, title_text_3d_left_pos)
        self.screen.blit(
            player_vs_player_text_3d_left, player_vs_player_text_3d_left_pos
        )
        self.screen.blit(player_vs_ai_text_3d_left, player_vs_ai_text_3d_left_pos)
        self.screen.blit(quit_text_3d_left, quit_text_3d_left_pos)
        self.screen.blit(player_vs_player_text, (350, 300))
        self.screen.blit(player_vs_ai_text, (390, 350))
        self.screen.blit(title_text, (240, 225))
        self.screen.blit(quit_text, (460, 400))

        pygame.display.update()

    def main_menu(self):
        self.player1_value = 0
        self.ai_value = 0
        self.node_expanded = 0
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.resize_game_window(event.w, event.h, -1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] > 300 and event.pos[1] < 350:
                        self.player_vs_player = True
                        self.menu = False
                    elif event.pos[1] > 350 and event.pos[1] < 400:
                        self.player_vs_player = False
                        self.menu = False
                        self.selected_ai_engine, self.difficulty = self.ai_menu()
                        print(self.selected_ai_engine)
                    elif event.pos[1] > 400 and event.pos[1] < 450:
                        pygame.quit()
                        sys.exit()

            self.screen.fill(BLACK)
            self.screen.blit(self.animation_frames[self.frame_index], (0, 0))
            self.clock.tick(10)
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.display_menu()

    def show_winner_popup(self, player):
        font = pygame.font.SysFont("monospace", 60, True)
        if player == -1:
            pygame.display.set_caption(f"It's a tie!")
            win_text = font.render(
                f"It's a tie!", True, GREEN if player == 1 else GREEN
            )
            self.screen.blit(win_text, (80, ROW_COUNT * SQUARE_SIZE // 2))

        elif self.player_vs_player:
            pygame.display.set_caption(f"Player {player} wins!")
            win_text = font.render(
                f"Player {player} wins!", True, GREEN if player == 1 else GREEN
            )
            self.screen.blit(win_text, (80, ROW_COUNT * SQUARE_SIZE // 2))

        else:
            win_text = font.render(f"AI wins!", True, GREEN)
            if player == "AI":
                pygame.display.set_caption("Computer Wins")
                win_text = font.render(
                    f"Computer wins!", True, GREEN if player == 1 else GREEN
                )
            else:
                pygame.display.set_caption("You Win")
                win_text = font.render(
                    f"You win!", True, GREEN if player == 1 else GREEN
                )
            self.screen.blit(win_text, (80, ROW_COUNT * SQUARE_SIZE // 2))
        font = pygame.font.SysFont("monospace", 30, True)
        fin_text = font.render(
            "Main menu press x, Quit press esc ", True, GREEN if player == 1 else GREEN
        )
        self.screen.blit(fin_text, (80, ROW_COUNT * SQUARE_SIZE // 2 + 100))
        pygame.display.update()
        pop_up = True
        while pop_up:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    self.menu = True
                    self.board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                    pop_up = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        self.main_menu()
        self.main()

    def draw_properties(self, turn):
        font = pygame.font.SysFont("monospace", 30, True)
        if self.player_vs_player:
            if turn == 1:
                turn_text = font.render("Player 1's turn", True, RED)
            else:
                turn_text = font.render("Player 2's turn", True, YELLOW)
        else:
            if turn == 1:
                turn_text = font.render("Your turn", True, RED)
            else:
                turn_text = font.render("AI's turn", True, YELLOW)
        player1Score = font.render(f"Your Score : {self.player1_value}", True, RED)
        aiScore = font.render(f"AI Score : {self.ai_value}", True, YELLOW)

        self.screen.blit(
            player1Score, ((COLUMN_COUNT) * SQUARE_SIZE + 10, 0 * SQUARE_SIZE + 30)
        )
        self.screen.blit(
            aiScore, ((COLUMN_COUNT) * SQUARE_SIZE + 10, 1 * SQUARE_SIZE + 30)
        )
        self.screen.blit(
            turn_text, ((COLUMN_COUNT) * SQUARE_SIZE + 10, 2 * SQUARE_SIZE)
        )
        if not self.player_vs_player:
            difficulty_text = font.render(
                f"AI DIFFICULTY {self.difficulty}", True, GREEN
            )
            self.screen.blit(
                difficulty_text, ((COLUMN_COUNT) * SQUARE_SIZE, 3 * SQUARE_SIZE)
            )
        pygame.display.update()

    def tie_move(self):
        for i in range(7):
            if self.is_valid_location(i):
                return False
        return True

    def main(self):
        turn = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.resize_game_window(event.w, event.h, turn)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player_vs_player:
                        col = event.pos[0] // SQUARE_SIZE
                        if col > 6:
                            continue
                        if self.is_valid_location(col):
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, turn + 1)
                            self.screen.fill(WHITE)
                            self.draw_board(turn + 1)
                            winning_move = self.check_is_winning_move(
                                turn + 1, col, row
                            )
                            if winning_move:
                                if turn == 0:
                                    self.player1_value += winning_move
                                else:
                                    self.ai_value += winning_move

                            if self.tie_move():
                                if self.player1_value > self.ai_value:
                                    self.show_winner_popup(1)
                                elif self.player1_value < self.ai_value:
                                    self.show_winner_popup(2)
                                else:
                                    self.show_winner_popup(-1)
                            turn = 1 - turn
                            continue
                    else:
                        if not self.menu:
                            col = event.pos[0] // SQUARE_SIZE
                            if col > 6:
                                continue
                            if self.is_valid_location(col):
                                row = self.get_next_open_row(col)
                                self.drop_piece(row, col, turn + 1)
                                self.screen.fill(WHITE)
                                self.draw_board(turn + 1)
                                winning_move = self.check_is_winning_move(
                                    turn + 1, col, row
                                )
                                if winning_move:
                                    self.player1_value += winning_move
                                if self.tie_move():
                                    if self.player1_value > self.ai_value:
                                        self.show_winner_popup(1)
                                    elif self.player1_value < self.ai_value:
                                        self.show_winner_popup("AI")
                                    else:
                                        self.show_winner_popup(-1)
                                turn = 1 - turn
                                continue
                elif not self.player_vs_player and turn == 1:
                    if not self.menu:
                        ai_col = self.ai_move()
                        ai_row = self.get_next_open_row(ai_col)
                        self.drop_piece(ai_row, ai_col, 2)
                        self.screen.fill(WHITE)
                        self.draw_board(turn)
                        winning_move = self.check_is_winning_move(2, ai_col, ai_row)
                        if winning_move:
                            self.ai_value += winning_move
                        if self.tie_move():
                            if self.player1_value > self.ai_value:
                                self.show_winner_popup(1)
                            elif self.player1_value < self.ai_value:
                                self.show_winner_popup("AI")
                            else:
                                self.show_winner_popup(-1)
                        turn = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.menu = True
                    self.board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                    turn = 0
                    self.player1_value = 0
                    self.ai_value = 0
                    self.main_menu()
            self.screen.fill(LIGHT_GRAY)
            self.draw_board(turn + 1)
            pygame.display.update()


if __name__ == "__main__":
    game = ConnectFour()
