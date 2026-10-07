import pygame
import random

pygame.init()

display_info = pygame.display.Info()

screen = pygame.display.set_mode(
    (display_info.current_w,
     display_info.current_h),
    pygame.NOFRAME
)

WIDTH = screen.get_width()
HEIGHT = screen.get_height()

pygame.display.set_caption("Tic Tac Toe")

font = pygame.font.SysFont(None, 120)
message_font = pygame.font.SysFont(None, 50)

particles = []
for i in range(40):
    particles.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed": random.uniform(0.2, 1.0),
        "size": random.randint(2, 5)
    })

board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]

selected_row = 0
selected_col = 0

player_symbol = "X"
computer_symbol = "O"

game_over = False
winner = None


def check_winner():

    # Check rows
    for row in board:
        if row[0] != "" and row[0] == row[1] == row[2]:
            return row[0]

    for col in range(3):
        if (
            board[0][col] != ""
            and board[0][col] == board[1][col] == board[2][col]
        ):
            return board[0][col]

    # Check main diagonal
    if (
        board[0][0] != ""
        and board[0][0] == board[1][1] == board[2][2]
    ):
        return board[0][0]

    # Check other diagonal
    if (
        board[0][2] != ""
        and board[0][2] == board[1][1] == board[2][0]
    ):
        return board[0][2]

    # Check tie
    filled = True

    for row in board:
        for cell in row:
            if cell == "":
                filled = False

    if filled:
        return "Tie"

    return None

def reset_game():
    global board
    global selected_row
    global selected_col
    global game_over
    global winner

    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    selected_row = 0
    selected_col = 0

    game_over = False
    winner = None


def computer_move():

    empty_cells = []

    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                empty_cells.append((row, col))

    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = computer_symbol


running = True

while running:

    screen.fill((20, 20, 40))

    for particle in particles:

        particle["y"] += particle["speed"]

        if particle["y"] > HEIGHT:
            particle["y"] = 0
            particle["x"] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            (100, 100, 160),
            (int(particle["x"]), int(particle["y"])),
            particle["size"]
        )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.K_q:
                running = False

            if game_over:
                if event.key == pygame.K_RETURN:
                    reset_game()

                elif event.key == pygame.K_ESCAPE:
                    running = False

                continue

            if event.key == pygame.K_LEFT:
                selected_col = max(0, selected_col - 1)

            elif event.key == pygame.K_RIGHT:
                selected_col = min(2, selected_col + 1)

            elif event.key == pygame.K_UP:
                selected_row = max(0, selected_row - 1)

            elif event.key == pygame.K_DOWN:
                selected_row = min(2, selected_row + 1)

            elif event.key == pygame.K_RETURN:

                if board[selected_row][selected_col] == "":

                    board[selected_row][selected_col] = player_symbol

                    result = check_winner()

                    if result:
                        game_over = True
                        winner = result

                    else:

                        computer_move()

                        result = check_winner()

                        if result:
                            game_over = True
                            winner = result

    cell_size = min(WIDTH, HEIGHT) // 6
    board_width = cell_size * 3
    board_height = cell_size * 3
    start_x = (WIDTH - board_width) // 2
    start_y = (HEIGHT - board_height) // 2 - 50
        

    #
    # draw cells
    #

    for row in range(3):
        for col in range(3):

            rect = pygame.Rect(
                start_x + col * cell_size,
                start_y + row * cell_size,
                cell_size,
                cell_size
            )

            pygame.draw.rect(
                screen,
                (120, 120, 120),
                rect,
                2
            )

            if row == selected_row and col == selected_col:
                pygame.draw.rect(
                    screen,
                    (255, 255, 0),
                    rect,
                    4
                )

            symbol = board[row][col]

            if symbol:

                text = font.render(
                    symbol,
                    True,
                    (255, 255, 255)
                )

                text_rect = text.get_rect(
                    center=rect.center
                )

                screen.blit(
                    text,
                    text_rect
                )

    #
    # status text
    #

    if game_over:

        if winner == "Tie":
            message = "Tie Game"
        else:
            message = f"{winner} Wins!"

        text = message_font.render(
            message,
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=(WIDTH // 2, HEIGHT - 150)
        )

        screen.blit(
            text,
            text_rect
        )

        restart_text = message_font.render(
            "ENTER = Play Again    ESC = Exit",
            True,
            (200, 200, 200)
        )

        restart_rect = restart_text.get_rect(
            center=(WIDTH // 2, HEIGHT - 100)
        )

        screen.blit(
            restart_text,
            restart_rect
        )

    else:

        message = "Arrow Keys + Enter | ESC = Exit"

        text = message_font.render(
            message,
            True,
            (255, 255, 255)
        )

        message_y = start_y + board_height + 60

        text_rect = text.get_rect(
            center=(WIDTH // 2, message_y)
        )

        screen.blit(
            text,
            text_rect
        )

    pygame.display.flip()


pygame.quit()