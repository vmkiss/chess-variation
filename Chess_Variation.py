import pygame

print(pygame.font.get_fonts())

pygame.init()
width = 800
height = 1000
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Chess Variation')
font = pygame.font.SysFont('courier', 20, True)
big_font = pygame.font.SysFont('courier', 30, True)
game_over_font = pygame.font.SysFont('courier', 60, True)
timer = pygame.time.Clock()
fps = 60

white_pieces = ['king', 'bishop', 'knight', 'castle', 'bishop', 'knight']
white_pos = [(0, 7), (1, 7), (2, 7), (0, 6), (1, 6), (2, 6)]
black_pieces = ['knight', 'bishop', 'king', 'knight', 'bishop', 'castle']
black_pos = [(5, 7), (6, 7), (7, 7), (5, 6), (6, 6), (7, 6)]

# Add images of game pieces and scale them to size of game board
b_bishop_img = pygame.image.load('images/black bishop.png')
b_bishop_img = pygame.transform.scale(b_bishop_img, (80, 80))
b_castle_img = pygame.image.load('images/black castle.png')
b_castle_img = pygame.transform.scale(b_castle_img, (80, 80))
b_king_img = pygame.image.load('images/black king.png')
b_king_img = pygame.transform.scale(b_king_img, (80, 80))
b_knight_img = pygame.image.load('images/black knight.png')
b_knight_img = pygame.transform.scale(b_knight_img, (80, 80))
black_imgs = [b_bishop_img, b_castle_img, b_king_img, b_knight_img]

w_bishop_img = pygame.image.load('images/white bishop.png')
w_bishop_img = pygame.transform.scale(w_bishop_img, (80, 80))
w_castle_img = pygame.image.load('images/white castle.png')
w_castle_img = pygame.transform.scale(w_castle_img, (80, 80))
w_king_img = pygame.image.load('images/white king.png')
w_king_img = pygame.transform.scale(w_king_img, (80, 80))
w_knight_img = pygame.image.load('images/white knight.png')
w_knight_img = pygame.transform.scale(w_knight_img, (80, 80))
white_imgs = [w_bishop_img, w_castle_img, w_king_img, w_knight_img]

piece_list = ['bishop', 'castle', 'king', 'knight']

turn_step = 0
selection = 100
winner = None

# Draw chess board
def draw_board():
    # Draw squares
    for i in range(32):
        col = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light blue', [600 - (col * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light blue', [700 - (col * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, width, 100])
        pygame.draw.rect(screen, 'tan', [0, 800, width, 100], 5)
        status_text = ['White: Select Your Piece!', 'White: Select a Destination!',
                       'Black: Select Your Piece!!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (180, 820))

        for i in range(9):
            pygame.draw.line(screen, 'tan', (0, 100 * i), (800, 100 * i), 3)
            pygame.draw.line(screen, 'tan', (100 * i, 0), (100 * i, 800), 3)

# Draw pieces on board
def draw_pieces():
    # Draw white pieces
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_imgs[index], (white_pos[i][0] * 100 + 10, white_pos[i][1] * 100 + 10))
        if turn_step <= 1:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_pos[i][0] * 100 + 1, white_pos[i][1] * 100 + 1,
                                                 100, 100], 2)

    # Draw black pieces
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_imgs[index], (black_pos[i][0] * 100 + 10, black_pos[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_pos[i][0] * 100 + 1, black_pos[i][1] * 100 + 1,
                                                  100, 100], 2)

def draw_game_over():
    pygame.draw.rect(screen, 'red', [200, 300, 400, 200])
    if winner == 'Tie':
        screen.blit(game_over_font.render("It's a tie!", True, 'white'), (205, 340))
    else:
        screen.blit(game_over_font.render(f'{winner} won!', True, 'white'), (225, 340))
    screen.blit(game_over_font.render(f'GAME OVER', True, 'white'), (240, 400))


def is_valid_move(start_pos_idx, end_coord, color):
    """Takes index of selected piece, player's desired end coordinates, and color of piece and returns
    a Boolean indicating whether the intended move is valid"""
    # Return False if intended move is beyond the bounds of the game board
    if end_coord[0] > 7 or end_coord[1] > 7:
        return False
    if verify_end_coord_occupiable(end_coord, color):
        if color == 'white':
            piece = white_pieces[start_pos_idx]
            start_coord = white_pos[start_pos_idx]
            if piece == 'bishop':
                return check_bishop(start_coord, end_coord)
            elif piece == 'castle':
                print("Checking castle")
                return check_castle(start_coord, end_coord)
            elif piece == 'king':
                return check_king(start_coord, end_coord)
            else:
                return check_knight(start_coord, end_coord)
        else:
            piece = black_pieces[start_pos_idx]
            start_coord = black_pos[start_pos_idx]
            if piece == 'bishop':
                return check_bishop(start_coord, end_coord)
            elif piece == 'castle':
                print("Checking castle")
                return check_castle(start_coord, end_coord)
            elif piece == 'king':
                return check_king(start_coord, end_coord)
            else:
                return check_knight(start_coord, end_coord)
    return False


def check_bishop(start_coord, end_coord):
    start_col = start_coord[0]
    start_row = start_coord[1]
    end_col = end_coord[0]
    end_row = end_coord[1]

    # A move is valid if the player moves the Bishop the same number of rows and columns
    if abs(start_row - end_row) == abs(start_col - end_col):
        return check_bishop_path_clear(start_col, start_row, end_col, end_row)
    # Return False if intended move not within Bishop's range
    return False

def check_bishop_path_clear(start_col, start_row, end_col, end_row):
    # Check upper left path
    if start_row > end_row and start_col > end_col:
        print("Checking upper left path")
        while start_row > end_row and start_col > end_col + 1:
            start_row -= 1
            start_col -= 1
            if (start_col, start_row) in white_pos or (start_col, start_row) in black_pos:
                return False
        print("Bishop move successful")
        return True
    # Check lower left path
    if start_row < end_row and start_col > end_col:
        print("Checking lower left path")
        while start_row < end_row - 1 and start_col > end_col + 1:
            start_row += 1
            start_col -= 1
            if (start_col, start_row) in white_pos or (start_col, start_row) in black_pos:
                return False
        print("Bishop move successful")
        return True
    # Check upper right path - CHECK FOR BUG CAUSING BISHOPS TO BE ABLE TO JUMP OVER PIECES
    if start_row > end_row and start_col < end_col:
        print("Checking upper right path")
        while start_row > end_row + 1 and start_col < end_col - 1:
            start_row -= 1
            start_col += 1
            if (start_col, start_row) in white_pos or (start_col, start_row) in black_pos:
                return False
        print("Bishop move successful")
        return True
    # Check lower right path - CHECK FOR BUG CAUSING BISHOPS TO BE ABLE TO JUMP OVER PIECES
    if start_row < end_row and start_col < end_col:
        print("Checking lower right path")
        while start_row < end_row - 1 and start_col < end_col - 1:
            start_row += 1
            start_col += 1
            if (start_col, start_row) in white_pos or (start_col, start_row) in black_pos:
                return False
        print("Bishop move successful")
        return True


def check_castle(start_coord, end_coord):
    start_col = start_coord[0]
    start_row = start_coord[1]
    end_col = end_coord[0]
    end_row = end_coord[1]

    # A Castle can move horizontally within its current row or vertically
    # within its current column
    if start_col == end_col or start_row == end_row:
        return check_castle_path_clear(start_col, start_row, end_col, end_row)
    # Return False if intended move not within Castle's range
    print("Move not in Castle range")
    return False


def check_castle_path_clear(start_col, start_row, end_col, end_row):
    # Check horizontal paths
    if start_row == end_row:
        # Check right path
        if start_col < end_col:
            # print("Checking right path")
            for col_num in range(start_col + 1, end_col):
                if (col_num, start_row) in white_pos or (col_num, start_row) in black_pos:
                    print("Castle path invalid")
                    return False
            print("Castle path valid")
            return True
        # Check left path
        if start_col > end_col:
            # print("Checking left path")
            for col_num in range(start_col - 1, end_col, -1):
                if (col_num, start_row) in white_pos or (col_num, start_row) in black_pos:
                    print("Castle path invalid")
                    return False
            print("Castle path valid")
            return True
    # Check vertical paths
    if start_col == end_col:
        # Check down path
        if start_row < end_row:
            # print("Checking down path")
            for row_num in range(start_row + 1, end_row):
                if (start_col, row_num) in white_pos or (start_col, row_num) in black_pos:
                    print("Castle path invalid")
                    return False
            print("Castle path valid")
            return True
        # Check up path
        if start_row > end_row:
            # print("Checking up path")
            for row_num in range(start_row - 1, end_row, -1):
                if (start_col, row_num) in white_pos or (start_col, row_num) in black_pos:
                    print("Castle path invalid")
                    return False
            print("Castle path valid")
            return True


def check_king(start_coord, end_coord):
    start_col = start_coord[0]
    start_row = start_coord[1]
    end_col = end_coord[0]
    end_row = end_coord[1]

    # Move is valid if King stays in same row and moves one column right or left
    if start_row == end_row and abs(start_col - end_col) == 1:
        print("Checking horizontal path")
        return True
    # Move is valid if King stays in same column and moves one row up or down
    if start_col == end_col and abs(start_row - end_row) == 1:
        print("Checking vertical path")
        return True
    # Move is valid if King moves one row up or down and one column right of left
    if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
        print("Checking diagonal path")
        return True
    return False


def check_knight(start_coord, end_coord):
    start_col = start_coord[0]
    start_row = start_coord[1]
    end_col = end_coord[0]
    end_row = end_coord[1]

    # Move is valid if Knight moves one row up or down and two columns right or left
    if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
        return True
    # Move is valid if Knight moves one column right or left and two rows up or down
    if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 2:
        return True
    # Otherwise move is invalid
    return False

def verify_end_coord_occupiable(end_coord, color):
    # If piece is white
    if color == 'white':
        # Return False if end coordinate is already occupied by a white piece
        if end_coord in white_pos:
            return False
        # Return False if end coord is occupied by the black king
        elif end_coord in black_pos:
            if black_pos.index(end_coord) == black_pieces.index('king'):
                return False
            # Return True if end coord occupied by other black piece
            return True
        # Return True if end coord unoccupied
        else:
            return True

    # If piece is black
    else:
        # Return False if end coordinate is already occupied by a black piece
        if end_coord in black_pos:
            return False
        elif end_coord in white_pos:
            # Return False if end coord is occupied by the white king
            if white_pos.index(end_coord) == white_pieces.index('king'):
                return False
            # Return True if end coord occupied by other white piece
            return True
        # Return True if end coord unoccupied
        else:
            return True

def check_if_game_won():
    w_king_idx = white_pieces.index('king')
    b_king_idx = black_pieces.index('king')
    w_king_pos = white_pos[w_king_idx]
    b_king_pos = black_pos[b_king_idx]

    # If white king in last row
    if w_king_pos[1] == 0:
        # If black king not in last row
        if b_king_pos[1] != 0:
            # White wins
            return 'White'
        # Game is tied if black king also in last row
        else:
            return 'Tie'
    else:
        # If black king in last row and white king not in last row, black wins
        if b_king_pos[1] == 0:
            return 'Black'


run = True
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()

    # Set up event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            print(click_coords)

            #If it's white's turn
            if turn_step <= 1:
                # If player clicks on square with white piece
                if click_coords in white_pos:
                    # Select white piece at that location
                    selection = white_pos.index(click_coords)
                    # Increment turn step
                    if turn_step == 0:
                        turn_step = 1
                # If player selects a valid destination square
                if selection != 100:
                    if is_valid_move(selection, click_coords, 'white'):
                        white_pos[selection] = click_coords
                        if click_coords in black_pos:
                            black_piece = black_pos.index(click_coords)
                            black_pieces.pop(black_piece)
                            black_pos.pop(black_piece)
                        turn_step = 2
                        selection = 100
            if turn_step > 1:
                # If player clicks on square with black piece
                if click_coords in black_pos:
                    # Select black piece at that location
                    selection = black_pos.index(click_coords)
                    # Increment turn step
                    if turn_step == 2:
                        turn_step = 3
                # If player selects a valid destination square
                if selection != 100:
                    if is_valid_move(selection, click_coords, 'black'):
                        black_pos[selection] = click_coords
                        if click_coords in white_pos:
                            index = white_pos.index(click_coords)
                            white_pieces.pop(index)
                            white_pos.pop(index)
                        turn_step = 0
                        selection = 100
                        print("Checking winner")
                        winner = check_if_game_won()
                        print(winner)

    if winner is not None:
        game_over = True
        draw_game_over()
    pygame.display.flip()
pygame.quit()