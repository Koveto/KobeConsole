import pygame
import random
import socket
from input_manager import *

HOSTNAME = socket.gethostname()
host_ip = ""
HOST_IP = ""
host_ip_input = ""
PORT = 5000
connected_players = 0
attempt_connection = False
server_socket = None
client_socket = None
joined_server = False
join_status = "Connection Failed"
is_hosting = False
my_symbol = ""
opponent_symbol = ""
my_turn = False
temp_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

temp_socket.connect(
    ("8.8.8.8", 80)
)

IP_ADDRESS = temp_socket.getsockname()[0]

temp_socket.close()

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

current_screen = "menu"

menu_options = [
    "Single Player",
    "LAN Multiplayer"
]

menu_index = 0

multiplayer_options = [
    "Host Game",
    "Join Game"
]

multiplayer_index = 0

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

def reset_multiplayer():

    global connected_players
    global attempt_connection
    global server_socket
    global client_socket
    global joined_server
    global join_status
    global is_hosting
    global my_symbol
    global opponent_symbol
    global my_turn

    connected_players = 0
    attempt_connection = False

    joined_server = False
    join_status = "Connection Failed"

    is_hosting = False

    my_symbol = ""
    opponent_symbol = ""

    my_turn = False

    if client_socket:
        try:
            client_socket.close()
        except OSError:
            pass

    if server_socket:
        try:
            server_socket.close()
        except OSError:
            pass

    client_socket = None
    server_socket = None

def get_ui_layout():

    return {
        "title_y": HEIGHT // 8,
        "symbol_y": HEIGHT // 5,
        "turn_y": HEIGHT // 5 + 50,
        "winner_y": HEIGHT - 150,
        "restart_y": HEIGHT - 100
    }

def draw_board(
    start_x,
    start_y,
    cell_size
):

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

            if (
                row == selected_row
                and col == selected_col
            ):
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

def swap_symbols():

    global my_symbol
    global opponent_symbol

    my_symbol, opponent_symbol = (
        opponent_symbol,
        my_symbol
    )

def get_board_layout():

    cell_size = min(WIDTH, HEIGHT) // 6

    board_width = cell_size * 3
    board_height = cell_size * 3

    start_x = (WIDTH - board_width) // 2
    start_y = (HEIGHT - board_height) // 2 + (HEIGHT // 20)

    return (
        cell_size,
        board_width,
        board_height,
        start_x,
        start_y
    )

def draw_footer(text):

    ui = get_ui_layout()

    footer = message_font.render(
        text,
        True,
        (200, 200, 200)
    )

    footer_rect = footer.get_rect(
        center=(WIDTH // 2, ui["restart_y"])
    )

    screen.blit(
        footer,
        footer_rect
    )


def swap_singleplayer_symbols():

    global player_symbol
    global computer_symbol

    player_symbol, computer_symbol = (
        computer_symbol,
        player_symbol
    )

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

    if current_screen == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if is_up(event):
                    menu_index = max(0, menu_index - 1)
                elif is_down(event):
                    menu_index = min(
                        len(menu_options) - 1,
                        menu_index + 1
                    )
                elif is_confirm(event):
                    if menu_index == 0:
                        current_screen = "singleplayer"
                    elif menu_index == 1:
                        current_screen = "lan_menu"
                elif event.key == pygame.K_q:
                    running = False
        title = font.render(
            "Tic Tac Toe",
            True,
            (255, 255, 255)
        )

        single_color = (
            (255, 255, 0)
            if menu_index == 0
            else (255, 255, 255)
        )

        option_text = message_font.render(
            "Single Player",
            True,
            single_color
        )

        multi_color = (
            (255, 255, 0)
            if menu_index == 1
            else (255, 255, 255)
        )

        multi_text = message_font.render(
            "LAN Multiplayer",
            True,
            multi_color
        )

        multi_rect = multi_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 60)
        )

        screen.blit(
            multi_text,
            multi_rect
        )

        option_rect = option_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

        screen.blit(
            option_text,
            option_rect
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, HEIGHT // 3)
        )

        screen.blit(
            title,
            title_rect
        )

        draw_footer(
            "UP/DOWN = Select   ENTER = Confirm   Q = Quit"
        )

    elif current_screen == "singleplayer":

        ui = get_ui_layout()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if is_cancel(event):
                    reset_game()
                    current_screen = "menu"

                elif event.key == pygame.K_q:
                    running = False

                if game_over:
                    if is_confirm(event):
                        swap_singleplayer_symbols()
                        reset_game()
                        if computer_symbol == "X":
                            computer_move()

                    continue

                if is_left(event):
                    selected_col = max(0, selected_col - 1)

                elif is_right(event):
                    selected_col = min(2, selected_col + 1)

                elif is_up(event):
                    selected_row = max(0, selected_row - 1)

                elif is_down(event):
                    selected_row = min(2, selected_row + 1)

                elif is_confirm(event):

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

        (
            cell_size,
            board_width,
            board_height,
            start_x,
            start_y
        ) = get_board_layout()
            

        #
        # draw cells
        #

        draw_board(
            start_x,
            start_y,
            cell_size
        )

        #
        # status text
        #

        if game_over:

            if winner == "Tie":
                message = "Tie Game"

            elif winner == player_symbol:
                message = "You Win!"

            else:
                message = "You Lose!"

            text = message_font.render(
                message,
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(
                center=(WIDTH // 2, ui["winner_y"])
            )

            screen.blit(
                text,
                text_rect
            )

            restart_text = message_font.render(
                "ENTER = Play Again    ESC = Menu",
                True,
                (200, 200, 200)
            )

            restart_rect = restart_text.get_rect(
                center=(WIDTH // 2, ui["restart_y"])
            )

            screen.blit(
                restart_text,
                restart_rect
            )

        else:

            draw_footer(
                "ARROWS = Move   ENTER = Place   ESC = Menu"
            )

    elif current_screen == "lan_menu":

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    running = False

                elif is_cancel(event):
                    
                    reset_game()
                    current_screen = "menu"

                elif is_up(event):
                    multiplayer_index = max(0, multiplayer_index - 1)

                elif is_down(event):
                    multiplayer_index = min(
                        1,
                        multiplayer_index + 1
                    )

                elif is_confirm(event):

                    if multiplayer_index == 0:
                        current_screen = "host"

                    elif multiplayer_index == 1:
                        current_screen = "join"
                


        title = font.render(
            "LAN Multiplayer",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, HEIGHT // 3)
        )

        screen.blit(
            title,
            title_rect
        )

        host_color = (
            (255, 255, 0)
            if multiplayer_index == 0
            else (255, 255, 255)
        )

        host_text = message_font.render(
            "Host Game",
            True,
            host_color
        )

        host_rect = host_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

        screen.blit(
            host_text,
            host_rect
        )

        join_color = (
            (255, 255, 0)
            if multiplayer_index == 1
            else (255, 255, 255)
        )

        join_text = message_font.render(
            "Join Game",
            True,
            join_color
        )

        join_rect = join_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 60)
        )

        screen.blit(
            join_text,
            join_rect
        )

        draw_footer(
            "UP/DOWN = Select   ENTER = Confirm   ESC = Back"
        )
    
    elif current_screen == "host":

        HOST_IP = IP_ADDRESS

        if not is_hosting:

            server_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            server_socket.bind(
                (IP_ADDRESS, PORT)
            )

            server_socket.listen(1)
            server_socket.setblocking(False)

            is_hosting = True

        if connected_players == 0:

            try:
                client_socket, address = server_socket.accept()
                client_socket.setblocking(False)

                connected_players = 1
                current_screen = "lan_game"
                my_symbol = "X"
                opponent_symbol = "O"
                my_turn = True

            except (
                BlockingIOError,
                ConnectionResetError,
                OSError
            ):
                pass

        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    running = False

                elif is_cancel(event):

                    reset_game()
                    reset_multiplayer()
                    current_screen = "lan_menu"


        connection_status = (
            "Hosting..."
            if is_hosting
            else "Not Hosting"
        )

        title = font.render(
            "Host Game",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, HEIGHT // 3)
        )

        screen.blit(
            title,
            title_rect
        )

        message = message_font.render(
            connection_status,
            True,
            (255, 255, 0)
        )

        message_rect = message.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

        screen.blit(
            message,
            message_rect
        )

        host_name_text = message_font.render(
            f"Host: {HOSTNAME}",
            True,
            (255, 255, 255)
        )

        host_name_rect = host_name_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 60)
        )

        screen.blit(
            host_name_text,
            host_name_rect
        )

        ip_text = message_font.render(
            f"IP: {IP_ADDRESS}",
            True,
            (255, 255, 255)
        )

        ip_rect = ip_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 120)
        )

        screen.blit(
            ip_text,
            ip_rect
        )

        port_text = message_font.render(
            f"Port: {PORT}",
            True,
            (255, 255, 255)
        )

        port_rect = port_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 180)
        )

        screen.blit(
            port_text,
            port_rect
        )

        players_text = message_font.render(
            f"Players Connected: {connected_players}",
            True,
            (255, 255, 255)
        )

        players_rect = players_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 240)
        )

        screen.blit(
            players_text,
            players_rect
        )

        draw_footer(
            "ESC = Back     Q = Quit"
        )


    elif current_screen == "join":
        if (
            attempt_connection
            and not joined_server
        ):


            try:

                client_socket = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )

                client_socket.settimeout(2)

                client_socket.connect(
                    (host_ip_input, PORT)
                )

                joined_server = True
                join_status = "Connected!"
                attempt_connection = False
                current_screen = "lan_game"
                my_symbol = "O"
                opponent_symbol = "X"
                my_turn = False

                client_socket.setblocking(False)

            except OSError:

                join_status = "Connection Failed"
                attempt_connection = False

        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    running = False

                elif is_cancel(event):
                    reset_game()
                    reset_multiplayer()
                    current_screen = "lan_menu"

                elif event.key == pygame.K_BACKSPACE:
                    host_ip_input = host_ip_input[:-1]

                elif is_confirm(event):
                    attempt_connection = True

                elif event.unicode in "0123456789.":
                    host_ip_input += event.unicode
        title = font.render(
            "Join Game",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, HEIGHT // 3)
        )

        screen.blit(
            title,
            title_rect
        )

        ip_prompt = message_font.render(
            f"Host IP: {host_ip_input}",
            True,
            (255, 255, 255)
        )

        ip_prompt_rect = ip_prompt.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 60)
        )

        screen.blit(
            ip_prompt,
            ip_prompt_rect
        )

        instruction_text = message_font.render(
            "Type Host IP Address",
            True,
            (200, 200, 200)
        )

        instruction_rect = instruction_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 120)
        )

        screen.blit(
            instruction_text,
            instruction_rect
        )

        connect_text = message_font.render(
            "ENTER = Connect",
            True,
            (200, 200, 200)
        )

        connect_rect = connect_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 120)
        )

        screen.blit(
            connect_text,
            connect_rect
        )

        message = message_font.render(
            join_status,
            True,
            (255, 255, 0)
        )

        message_rect = message.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

        screen.blit(
            message,
            message_rect
        )

        draw_footer(
            "ENTER = Connect   ESC = Back   Q = Quit"
        )
    
    elif current_screen == "lan_game":

        ui = get_ui_layout()

        try:

            message = client_socket.recv(
                1024
            ).decode()

            if message.startswith("MOVE:"):

                move_data = message.replace(
                    "MOVE:",
                    ""
                )

                row, col = move_data.split(",")

                row = int(row)
                col = int(col)

                board[row][col] = opponent_symbol
                result = check_winner()

                if result:
                    game_over = True
                    winner = result

                my_turn = True

            elif message == "TURN":

                my_turn = True

            elif message == "RESET":

                swap_symbols()
                reset_game()

        except (
            BlockingIOError,
            ConnectionResetError,
            OSError
        ):
            pass

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    running = False

                elif is_cancel(event):
                    
                    reset_game()
                    reset_multiplayer()
                    current_screen = "menu"

                if game_over:
                    if is_confirm(event):
                        swap_symbols()
                        reset_game()
                        client_socket.send(
                            "RESET".encode()
                        )

                    continue
                if is_left(event):
                    selected_col = max(0, selected_col - 1)

                elif is_right(event):
                    selected_col = min(2, selected_col + 1)

                elif is_up(event):
                    selected_row = max(0, selected_row - 1)

                elif is_down(event):
                    selected_row = min(2, selected_row + 1)

                elif is_confirm(event):

                    if (
                        my_turn
                        and board[selected_row][selected_col] == ""
                    ):

                        board[selected_row][selected_col] = my_symbol
                        result = check_winner()

                        if result:
                            game_over = True
                            winner = result

                        client_socket.send(
                            f"MOVE:{selected_row},{selected_col}".encode()
                        )

                        my_turn = False

        title = font.render(
            "LAN Game",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                WIDTH // 2,
                ui["title_y"]
            )
        )

        screen.blit(
            title,
            title_rect
        )

        (
            cell_size,
            board_width,
            board_height,
            start_x,
            start_y
        ) = get_board_layout()
            

        #
        # draw cells
        #

        draw_board(
            start_x,
            start_y,
            cell_size
        )

        #
        # status text
        #

        if game_over:

            if winner == "Tie":
                message = "Tie Game"

            elif winner == my_symbol:
                message = "You Win!"

            else:
                message = "You Lose!"

            text = message_font.render(
                message,
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(
                center=(WIDTH // 2, ui["winner_y"])
            )

            screen.blit(
                text,
                text_rect
            )

            restart_text = message_font.render(
                "ENTER = Play Again    ESC = Menu",
                True,
                (200, 200, 200)
            )

            restart_rect = restart_text.get_rect(
                center=(WIDTH // 2, ui["restart_y"])
            )

            screen.blit(
                restart_text,
                restart_rect
            )

        else:

            draw_footer(
                "ARROWS = Move   ENTER = Place   ESC = Menu"
            )

        

        if not game_over:

            symbol_text = message_font.render(
                f"You are {my_symbol}",
                True,
                (255, 255, 255)
            )
    
            symbol_rect = symbol_text.get_rect(
                center=(
                    WIDTH // 2,
                    ui["symbol_y"]
                )
            )
    
            screen.blit(
                symbol_text,
                symbol_rect
            )

            turn_text = message_font.render(
                (
                    "Your Turn"
                    if my_turn
                    else "Opponent's Turn"
                ),
                True,
                (255, 255, 0)
            )

            turn_rect = turn_text.get_rect(
                center=(
                    WIDTH // 2,
                    ui["turn_y"]
                )
            )

            screen.blit(
                turn_text,
                turn_rect
            )
        
        
    pygame.display.flip()


pygame.quit()