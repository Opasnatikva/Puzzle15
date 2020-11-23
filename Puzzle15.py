import copy
import random

BOARD_SIZE = 4
BLANK_STATE = '  '
solved = False


def generate_board(size=BOARD_SIZE):
    """Create a list of lists according to the desired board size"""
    board = []
    for index in range(size):
        board.append([])
        for col_index in range(size):
            board[index].append(BLANK_STATE)
    return board


def print_board(board):
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
    square_coors = []
    for row_index in range(len(board)):
        col_index = board[row_index].index(BLANK_STATE) if value in board[row_index] else None
        if col_index is not None:
            square_coors.append(row_index)
            square_coors.append(col_index)
            return square_coors


"""We need to find the empty square, find the origin square of the number, then shift the empty square a number of times
to move the number to the final position. We need to consider the unintended shift of other numbers on the board."""


def self_solving_structure(board, size, empty_square_coors):
    """Cycle through the numbers from 1 to size squared minus one, then evaluate the position of the current number.
    If the number is not one of the last two on a row, call the general placement function.
    If it is one of the last two numbers on a row, call the last two columns placement function.
    If it is in the last two rows of the board, call the finish sorting function."""
    for number in range(1, size * size):
        if number + (2 * size) > size * size:
            pass
        elif number / size == 0:
            pass
        elif (number - 1) / size == 0:
            pass
        else:
            move_on_board(board, "awddsa", empty_square_coors)


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


def move_on_board(board, sequence, empty_square_coors):
    """Take random string and scramble the board."""
    for index in sequence:
        board, empty_square_coors[0], empty_square_coors[1] = move(board, index, empty_square_coors)
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
    empty_x = empty_square_coors[0]
    empty_y = empty_square_coors[1]
    if direction == 'w' and empty_square_coors[1] < (BOARD_SIZE - 1):
        empty_y = move_up(board, empty_square_coors)
    elif direction == "s" and empty_square_coors[1] > 0:
        empty_y = move_down(board, empty_square_coors)
    elif direction == "a" and empty_square_coors[0] < (BOARD_SIZE - 1):
        empty_x = move_left(board, empty_square_coors)
    elif direction == "d" and empty_square_coors[0] > 0:
        empty_x = move_right(board, empty_square_coors)

    return board, empty_x, empty_y


def main():
    board = generate_board()
    board = populate_board(board)
    solution = copy.deepcopy(board)
    empty_square_coors = find_specific_square(board, BLANK_STATE)
    board, empty_square_coors = move_on_board(board, generate_random_string(), empty_square_coors)
    print_board(board)
    while not compare_to_solution(board, solution):
        direction = input_and_border_check(empty_square_coors)
        board, empty_square_coors[0], empty_square_coors[1] = move(board, direction, empty_square_coors)
        print_board(board)
    print("Congratulations!")


if __name__ == '__main__':
    main()

"""Move да приема само direction string и ако е грешен, да не го изпълнява, 
така когато randomize-ваме няма да имаме проблеми с boundary когато вкараме random стринг от asdwasdwasdwad..."""
