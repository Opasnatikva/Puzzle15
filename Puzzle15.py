import random

BOARD_SIZE = 4
BLANK_STATE = '  '


def generate_board(size=BOARD_SIZE):
    """Create a list of lists according to the desired board size"""
    board = []
    for index in range(size):
        board.append([])
        for col_index in range(size):
            board[index].append(BLANK_STATE)
    return board


def print_board(board):
    for index in range(len(board)):
        print(board[index])


def number_sequence(size=BOARD_SIZE):
    """Creates a serial list of numbers with length equal to the number of fields on the board.
    This list will be used to populate the board, 0 is replaced with two blank spaces to retain formatting."""
    list_of_numbers = [BLANK_STATE]
    for index in range(1, (size * size)):
        list_of_numbers.append(format(index, '02d'))
    return list_of_numbers


def generate_new_random_number(numbers):
    """Chooses a number from the list at random and deletes it from the list"""
    number = random.choice(numbers)
    numbers.remove(number)
    return number


def populate_board(board):
    """Initiate the number sequence, then cycle through the cells of the board, and populate them with it"""
    numbers = number_sequence()
    for row_index in range(len(board)):
        for col_index in range(len(board)):
            board[row_index][col_index] = generate_new_random_number(numbers)


def find_empty_square(board):
    for col_index in range(len(board)):
        for row_index in range(len(board)):
            if board[col_index][row_index] == BLANK_STATE:
                return row_index, col_index


def user_input():
    correct_input = False
    while not correct_input:
        direction = input("Please select which direction your desired would have to move"
                          " in order to fill the empty square! W for up, S for down, A for left, and D for right.")
        direction = direction.lower()
        if direction == "w" or "a" or "s" or "d":
            correct_input = True
    return direction


def input_and_border_check(empty_square_x, empty_square_y):
    correct_input = False
    while not correct_input:
        direction = user_input()
        if direction == 'w':
            if empty_square_y < 1:
                break
        elif direction == "s":
            if empty_square_y > (BOARD_SIZE - 1):
                break
        elif direction == "a":
            if empty_square_x < 1:
                break
        elif direction == "d":
            if empty_square_x > (BOARD_SIZE - 1):
                break
    return direction


def move(board, empty_square_x, empty_square_y,):
    direction = input_and_border_check(empty_square_x, empty_square_y)
    if direction == 'w':
        board[empty_square_x][empty_square_y] = board[empty_square_x][empty_square_y + 1]
        board[empty_square_x][empty_square_y + 1] = BLANK_STATE
    elif direction == "s":
        board[empty_square_x][empty_square_y] = board[empty_square_x][empty_square_y - 1]
        board[empty_square_x][empty_square_y - 1] = BLANK_STATE
    elif direction == "a":
        board[empty_square_x][empty_square_y] = board[empty_square_x - 1][empty_square_y]
        board[empty_square_x - 1][empty_square_y] = BLANK_STATE
    elif direction == "d":
        board[empty_square_x][empty_square_y] = board[empty_square_x + 1][empty_square_y]
        board[empty_square_x + 1][empty_square_y] = BLANK_STATE


def main():
    board = generate_board()
    populate_board(board)
    print_board(board)
    empty_square_x = find_empty_square(board)[0]
    empty_square_y = find_empty_square(board)[1]
    print(find_empty_square(board))
    move(board, empty_square_x, empty_square_y)
    print_board(board)

if __name__ == '__main__':
    main()
