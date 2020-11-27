import copy
import random

BOARD_SIZE = 4
BLANK_STATE = '  '
solved = False
BLANK_LEFT = 'd'
BLANK_UP = 's'
BLANK_RIGHT = 'a'
BLANK_DOWN = 'w'
LEFT_TO_TOP = 'waassd'
RIGHT_TO_TOP = 'sd'
TOP_TO_RIGHT = 'aw'
BOTTOM_TO_RIGHT = 'as'
RETURN_BLANK_LEFT = 'wdds'
RETURN_BLANK_ABOVE = 'assd'
RETURN_BLANK_RIGHT = 'waas'
RETURN_BLANK_BELOW = 'awwd'


def generate_board(size=BOARD_SIZE):
    """Create a list of lists according to the desired board size"""
    board = []
    for index in range(size):
        board.append([])
        for col_index in range(size):
            board[index].append(BLANK_STATE)
    return board


def print_board(board):
    print('')
    for row_index in range(len(board)):
        row = []
        for col_index in range(len(board)):
            row.append(board[col_index][row_index])
        print(row)


def number_sequence(size=BOARD_SIZE):
    """Creates a serial list of numbers with length equal to the number of fields on the board.
    This list will be used to populate the board, 0 is replaced with two blank spaces to retain formatting."""
    list_of_numbers = []
    for index in range(1, (size * size)):
        list_of_numbers.append(format(index, '02d'))
    list_of_numbers.append(BLANK_STATE)
    return list_of_numbers


def compare_to_solution(current_state, solved_state):
    if current_state == solved_state:
        return True


def populate_board(board):
    """Initiate the number sequence, then cycle through the cells of the board, and populate them with it"""
    numbers = number_sequence()
    for col_index in range(len(board)):
        for row_index in range(len(board)):
            board[row_index][col_index] = numbers[0]
            numbers.remove(numbers[0])
    return board


def find_specific_square(board, value):
    """Every move is based on the program having information on the coordinates of the empty space.
    The space is indexed once, then kept track of during each move."""
    """In order for the puzzle to be solved automatically, we need it to be able to analyze the board, and find the
    values it needs in order to then set them in the correct places."""
    square_coors = []  # Initiate empty array to append the two coordinates to
    for row_index in range(len(board)):
        col_index = board[row_index].index(value) if value in board[row_index] else None
        if col_index is not None:
            square_coors.append(row_index)
            square_coors.append(col_index)
            return square_coors


"""We need to find the empty square, find the origin square of the number, then shift the empty square a number of times
to move the number to the final position. We need to consider the unintended shift of other numbers on the board."""


def set_blank_space(board, number_coors, empty_square_coors):
    """Move empty square immediately above, below, to the left, or to the right from the active number"""
    if empty_square_coors[1] < number_coors[1]:  # If the empty square is above the number
        if number_coors[0] != empty_square_coors[0]:  # If the number is not in the same column as the empty space
            while empty_square_coors[1] < (number_coors[1]):  # While the empty square is above
                # the number (until they are on the same row)
                board, empty_square_coors = move(board, BLANK_DOWN, empty_square_coors)  # Move the empty square down
        else:
            while empty_square_coors[1] < (number_coors[1] - 1):  # While the empty square is more than
                # one above the number (until they are one above the other)
                board, empty_square_coors = move(board, BLANK_DOWN, empty_square_coors)  # Move the empty square down
    elif empty_square_coors[1] > number_coors[1]:  # If the empty square is below the number
        if number_coors[0] != empty_square_coors[0]:  # If the number is not in the same column
            while empty_square_coors[1] > (number_coors[1]):  # While the empty square is below the number
                # (until they are on the same row)
                board, empty_square_coors = move(board, BLANK_UP, empty_square_coors)  # Move the empty square up
        else:
            while empty_square_coors[1] > (number_coors[1] + 1):  # While the empty square is more than
                # one below the number (until they are one above the other)
                board, empty_square_coors = move(board, BLANK_UP, empty_square_coors)  # Move the empty square up
    """move empty square immediate to the left or right from the active number"""
    while empty_square_coors[0] > number_coors[0] + 1:  # Empty square is further than immediately to the right
        board, empty_square_coors = move(board, BLANK_LEFT, empty_square_coors)  # Move the empty square up
    while empty_square_coors[0] < number_coors[0] - 1:  # Empty square is further than immediately to the left
        board, empty_square_coors = move(board, BLANK_RIGHT, empty_square_coors)  # Move the empty square up
    print_board(board)
    return board, empty_square_coors  # We return the new board state, and the new coordinates of the empty space


def not_leftmost_col(board, number_coors, empty_square_coors, target_coors):
    if number_coors[0] == 0:  # If the number is in the leftmost column
        while number_coors[0] < target_coors[0]:
            if empty_square_coors[1] == number_coors[1] - 1:  # If the empty square is above the number
                board, empty_square_coors = move(board, TOP_TO_RIGHT, empty_square_coors)  # Move the empty square
                # immediately to the right from the number
            elif number_coors[1] == number_coors[1] + 1:  # If the empty square is below the number
                board, empty_square_coors = move(board, BOTTOM_TO_RIGHT, empty_square_coors)  # Move the empty square
                # immediately to the right from the number
    return board, empty_square_coors


def not_bottom_two_rows(board, number_coors, empty_square_coors):
    if number_coors[1] == BOARD_SIZE - 1:  # If the number is on the bottom row
        if empty_square_coors[0] == number_coors[0] - 1:  # If empty square adjacent left from number
            board, empty_square_coors = move(board, BLANK_RIGHT, empty_square_coors)
            board, empty_square_coors = move(board, RIGHT_TO_TOP, empty_square_coors)
            board, empty_square_coors = move(board, BLANK_DOWN, empty_square_coors)
        elif empty_square_coors[0] == number_coors[0] + 1:  # If empty square adjacent right from number
            board, empty_square_coors = move(board, RIGHT_TO_TOP, empty_square_coors)
            board, empty_square_coors = move(board, BLANK_DOWN, empty_square_coors)
            print_board(board)
    return board, empty_square_coors


def set_empty_square_left(board, empty_square_coors, number_coors):
    if empty_square_coors[0] == number_coors[0]:
        if empty_square_coors[1] > number_coors[1]:
            board, empty_square_coors = make_multiple_moves(board, 'ds', empty_square_coors)
        else:
            board, empty_square_coors = make_multiple_moves(board, 'awwdds', empty_square_coors)
    elif empty_square_coors[0] > number_coors[0]:
        board, empty_square_coors = make_multiple_moves(board, BLANK_LEFT, empty_square_coors)
    return board, empty_square_coors


def set_empty_square_right(board, empty_square_coors, number_coors):
    if empty_square_coors[0] == number_coors[0]:
        if empty_square_coors[1] > number_coors[1]:
            board, empty_square_coors = make_multiple_moves(board, 'as', empty_square_coors)
        else:
            board, empty_square_coors = make_multiple_moves(board, 'aw', empty_square_coors)
    elif empty_square_coors[0] < number_coors[0]:
        board, empty_square_coors = make_multiple_moves(board, BLANK_RIGHT, empty_square_coors)
    return board, empty_square_coors


def set_empty_square_up(board, empty_square_coors, number_coors):
    if empty_square_coors[0] == number_coors[0]:
        if empty_square_coors[1] > number_coors[1]:
            board, empty_square_coors = make_multiple_moves(board, BLANK_UP, empty_square_coors)
        else:
            return board, empty_square_coors
    elif empty_square_coors[0] < number_coors[0]:
        board, empty_square_coors = make_multiple_moves(board, LEFT_TO_TOP, empty_square_coors)
    elif empty_square_coors[0] > number_coors[0]:
        board, empty_square_coors = make_multiple_moves(board, RIGHT_TO_TOP, empty_square_coors)
    return board, empty_square_coors


def set_empty_square_down(board, empty_square_coors, number_coors):
    if empty_square_coors[0] == number_coors[0]:
        if empty_square_coors[1] > number_coors[1]:
            board, empty_square_coors = make_multiple_moves(board, 'as', empty_square_coors)
        else:
            board, empty_square_coors = make_multiple_moves(board, 'aw', empty_square_coors)
    elif empty_square_coors[0] < number_coors[0]:
        board, empty_square_coors = make_multiple_moves(board, BLANK_RIGHT, empty_square_coors)
    return board, empty_square_coors


def set_directional_blank(board, direction, empty_square_coors, number_coors):
    if direction == 'left':
        set_empty_square_left(board, empty_square_coors, number_coors)
    elif direction == 'right':
        set_empty_square_right(board, empty_square_coors, number_coors)
    elif direction == 'up':
        set_empty_square_up(board, empty_square_coors, number_coors)
    elif direction == 'down':
        set_empty_square_down(board, empty_square_coors, number_coors)
    return board, empty_square_coors


def set_number_in_place(board, number_coors, empty_square_coors, target_coors):
    """Move number away from the leftmost column unless the target is there"""
    board, empty_square_coors = not_leftmost_col(board, number_coors, empty_square_coors, target_coors)
    """Move number away from the bottom row"""
    board, empty_square_coors = not_bottom_two_rows(board, number_coors, empty_square_coors)
    """Move active number to goal column"""
    if number_coors[0] > target_coors[0]:  # If the number is further right than the target square
        set_directional_blank(board, 'left', empty_square_coors, number_coors)
        same_column = False
        while not same_column:
            board, empty_square_coors = move(board, BLANK_RIGHT, empty_square_coors)
            if number_coors[0] == target_coors[0]:
                same_column = True
            else:
                board, empty_square_coors = make_multiple_moves(board, RETURN_BLANK_LEFT, empty_square_coors)
            print_board(board)
    elif number_coors[0] < target_coors[0]:
        same_column = False
        while not same_column:
            board, empty_square_coors = move(board, BLANK_LEFT, empty_square_coors)
            if number_coors[0] == target_coors[0]:
                same_column = True
            else:
                board, empty_square_coors = move(board, RETURN_BLANK_RIGHT, empty_square_coors)
            print_board(board)
    """Move active number to goal row"""
    if number_coors[1] > target_coors[1]:
        same_row = False
        while not same_row:
            board, empty_square_coors = move(board, BLANK_DOWN, empty_square_coors)
            if number_coors[1] > target_coors[1]:
                board, empty_square_coors = move(board, RETURN_BLANK_ABOVE, empty_square_coors)
            else:
                same_row = True
            print_board(board)
    elif number_coors[1] < target_coors[1]:
        same_row = False
        while not same_row:
            board, empty_square_coors = move(board, BLANK_UP, empty_square_coors)
            if number_coors[1] < target_coors[1]:
                board, empty_square_coors = move(board, RETURN_BLANK_BELOW, empty_square_coors)
            else:
                same_row = True
        print_board(board)
    return board, empty_square_coors


def self_solving_structure(board, solution):
    """Cycle through the numbers from 1 to size squared minus one, then evaluate the position of the current number.
    If the number is not one of the last two on a row, call the general placement function.
    If it is one of the last two numbers on a row, call the last two columns placement function.
    If it is in the last two rows of the board, call the finish sorting function."""
    empty_square_coors = find_specific_square(board, BLANK_STATE)
    for number in range(1, BOARD_SIZE * BOARD_SIZE):
        number_as_string = format(number, '02d')
        target_coors = find_specific_square(solution, number_as_string)
        number_coors = find_specific_square(board, number_as_string)
        if number + (2 * BOARD_SIZE) > BOARD_SIZE * BOARD_SIZE:
            """Find the first numbers of the last two columns, and set them in their places"""
            """Wiggle the other numbers around randomly, until it is solved."""
            pass
        elif (number + 1) % BOARD_SIZE == 0:  # Деление с остатък МАДАФАКА!!!
            """set the final number first"""
            one_plus_number_as_string = str(number).format(number + 1, '02d')
            number_coors = find_specific_square(board,
                                                one_plus_number_as_string)  # Take the coors of the last num on the row
            board, empty_square_coors = set_blank_space(board, number_coors,
                                                        empty_square_coors)  # Set the blank space to the left of target
            board, empty_square_coors = set_number_in_place(board, number_coors, empty_square_coors, target_coors)
            """Set the previous number on the square below it"""
            number_coors = find_specific_square(board, number_as_string)
            target_coors[1] += 1
            board, empty_square_coors = set_blank_space(board, number_coors, empty_square_coors)
            board, empty_square_coors = set_number_in_place(board, number_coors, empty_square_coors, target_coors)
            """shift them clockwise so they set in place"""
            board, empty_square_coors = make_multiple_moves(board, 'assdw', empty_square_coors)
        else:  # Number is not in the last two columns or last two rows
            board, empty_square_coors = set_blank_space(board, number_coors, empty_square_coors)
            board, empty_square_coors = set_number_in_place(board, number_coors, empty_square_coors, target_coors)
    print_board(board)


def method_choice(grid, number):
    """Function to determine which part of the algorithm to use to place the number, based on whether it is in the last
    2 columns or not, and whether it is in the last 2 rows or not."""
    square_coors = []
    square_coors[0], square_coors[1] = find_specific_square(grid, number)
    return square_coors


def generate_random_string():
    """Generate a string of random letters with a random length to make every game start differently.
    The String is used in the Randomize function"""
    random_string = ''
    for _ in range(random.randrange(200, 500)):
        random_string += random.choice(['w', 'a', 's', 'd'])
    return random_string


def make_multiple_moves(board, sequence, empty_square_coors):
    """Take random string and scramble the board."""
    for index in sequence:
        board, empty_square_coors = move(board, index, empty_square_coors)
    return board, empty_square_coors


def input_and_border_check(empty_square_coors):
    """Take input from user, checks if what is provided is a single directional letter,
     and checks whether the move would be appropriate for the current blank field"""
    direction = ''
    correct_input = False
    while not correct_input:
        direction = input("Please select which direction your desired would have to move"
                          " in order to fill the empty square! W for up, S for down, A for left, and D for right.")
        direction = direction.lower()
        if direction == 's':
            if empty_square_coors[1] > 0:
                correct_input = True
        elif direction == 'w':
            if empty_square_coors[1] < (BOARD_SIZE - 1):
                correct_input = True
        elif direction == 'd':
            if empty_square_coors[0] > 0:
                correct_input = True
        elif direction == 'a':
            if empty_square_coors[0] < (BOARD_SIZE - 1):
                correct_input = True
        else:
            direction = 'exception'
    return direction


def move_left(board, empty_square_coors):
    """Overwrite blank space with value from relevant field, overwrite the adjacent relevant field with BLANK_SPACE
    return relevant coordinate to update the location of the blank field"""
    board[empty_square_coors[0]][empty_square_coors[1]] = board[empty_square_coors[0] + 1][empty_square_coors[1]]
    board[empty_square_coors[0] + 1][empty_square_coors[1]] = BLANK_STATE
    return empty_square_coors[0] + 1


def move_right(board, empty_square_coors):
    """Overwrite blank space with value from relevant field, overwrite the adjacent relevant field with BLANK_SPACE
        return relevant coordinate to update the location of the blank field"""
    board[empty_square_coors[0]][empty_square_coors[1]] = board[empty_square_coors[0] - 1][empty_square_coors[1]]
    board[empty_square_coors[0] - 1][empty_square_coors[1]] = BLANK_STATE
    return empty_square_coors[0] - 1


def move_up(board, empty_square_coors):
    """Overwrite blank space with value from relevant field, overwrite the adjacent relevant field with BLANK_SPACE
        return relevant coordinate to update the location of the blank field"""
    board[empty_square_coors[0]][empty_square_coors[1]] = board[empty_square_coors[0]][empty_square_coors[1] + 1]
    board[empty_square_coors[0]][empty_square_coors[1] + 1] = BLANK_STATE
    return empty_square_coors[1] + 1


def move_down(board, empty_square_coors):
    """Overwrite blank space with value from relevant field, overwrite the adjacent relevant field with BLANK_SPACE
        return relevant coordinate to update the location of the blank field"""
    board[empty_square_coors[0]][empty_square_coors[1]] = board[empty_square_coors[0]][empty_square_coors[1] - 1]
    board[empty_square_coors[0]][empty_square_coors[1] - 1] = BLANK_STATE
    return empty_square_coors[1] - 1


def move(input_board, direction, empty_square_coors):
    """Takes the board, and the empty square, and based on the input calls the relevant directional move function,
    then returns the new board state and the updated coordinates of the empty field"""
    board = input_board.copy()
    empty_coors = ['', '']
    empty_coors[0] = empty_square_coors[0]
    empty_coors[1] = empty_square_coors[1]
    if direction == 'w' and empty_square_coors[1] < (BOARD_SIZE - 1):
        empty_coors[1] = move_up(board, empty_square_coors)
    elif direction == "s" and empty_square_coors[1] > 0:
        empty_coors[1] = move_down(board, empty_square_coors)
    elif direction == "a" and empty_square_coors[0] < (BOARD_SIZE - 1):
        empty_coors[0] = move_left(board, empty_square_coors)
    elif direction == "d" and empty_square_coors[0] > 0:
        empty_coors[0] = move_right(board, empty_square_coors)

    return board, empty_coors


def main():
    board = populate_board(generate_board())
    solution = copy.deepcopy(board)
    empty_square_coors = find_specific_square(board, BLANK_STATE)
    board, empty_square_coors = make_multiple_moves(board, generate_random_string(), empty_square_coors)
    print_board(board)
    while not compare_to_solution(board, solution):
        self_solving_structure(board, solution)
        # direction = input_and_border_check(empty_square_coors)
        # board, empty_square_coors = move(board, direction, empty_square_coors)
        print_board(board)
    print("Congratulations!")


if __name__ == '__main__':
    main()

"""позиционирането на празното поле отляво създава проблем когато стойността е в първата колона.
Потенциално решение е да се направи условие когато има такъв сценарий, полето да застава отдясно
и да започва местенето оттам"""
