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


def puzzle_state(board, size=BOARD_SIZE):
    """Takes the nested lists and arranges all values in a single list in order to then compare them to the solution"""
    order = []
    for row_index in range(size):
        order.append([])
        for col_index in range(size):
            order.append(board[row_index][col_index])
    return order


def compare_to_solution(puzzle_state, number_sequence):
    if puzzle_state == number_sequence:
        return True


# def generate_new_random_number(numbers):
#     """Chooses a number from the list at random and deletes it from the list"""
#     number = random.choice(numbers)
#     numbers.remove(number)
#     return number


def populate_board(board):
    """Initiate the number sequence, then cycle through the cells of the board, and populate them with it"""
    numbers = number_sequence()
    for col_index in range(len(board)):
        for row_index in range(len(board)):
            board[row_index][col_index] = numbers[0]
            numbers.remove(numbers[0])


def find_empty_square(board):
    for row_index in range(len(board)):
        for col_index in range(len(board)):
            if board[row_index][col_index] == BLANK_STATE:
                return row_index, col_index


def shuffle_input():
    random_moves = input("insert as many WASD letters as you want in order to shuffle the board")
    return random_moves.lower()


def generate_random_string():
    string = ''
    for index in range(random.randrange(100,250)):
        string += random.choice(['w', 'a', 's', 'd'])
    return string


def randomize(board, sequence, empty_square_x, empty_square_y):
    for index in sequence:
        empty_square_x, empty_square_y = move(board, index, empty_square_x, empty_square_y)


def input_and_border_check(empty_square_x, empty_square_y):
    """Take input from user, checks if what is provided is a single directional letter,
     and checks whether the move would be appropriate for the current blank field"""
    correct_input = False
    while not correct_input:
        direction = input("Please select which direction your desired would have to move"
                          " in order to fill the empty square! W for up, S for down, A for left, and D for right.")
        direction = direction.lower()
        if direction == 's':
            if empty_square_y > 0:
                correct_input = True
        elif direction == 'w':
            if empty_square_y < (BOARD_SIZE - 1):
                correct_input = True
        elif direction == 'd':
            if empty_square_x > 0:
                correct_input = True
        elif direction == 'a':
            if empty_square_x < (BOARD_SIZE - 1):
                correct_input = True
        else:
            direction = 'exception'
    return direction


def move(board, direction, empty_square_x, empty_square_y):
    """Takes the board, and the empty square, and based on the input overwrites the value of the empty square,
     and makes the source field the new empty field"""
    empty_x = empty_square_x
    empty_y = empty_square_y
    if direction == 'w' and empty_square_y < (BOARD_SIZE - 1):
        board[empty_square_x][empty_square_y] = board[empty_square_x][empty_square_y + 1]
        board[empty_square_x][empty_square_y + 1] = BLANK_STATE
        empty_y = empty_square_y + 1
    elif direction == "s" and empty_square_y > 0:
        board[empty_square_x][empty_square_y] = board[empty_square_x][empty_square_y - 1]
        board[empty_square_x][empty_square_y - 1] = BLANK_STATE
        empty_y = empty_square_y - 1
    elif direction == "a" and empty_square_x < (BOARD_SIZE - 1):
        board[empty_square_x][empty_square_y] = board[empty_square_x + 1][empty_square_y]
        board[empty_square_x + 1][empty_square_y] = BLANK_STATE
        empty_x = empty_square_x + 1
    elif direction == "d" and empty_square_x > 0:
        board[empty_square_x][empty_square_y] = board[empty_square_x - 1][empty_square_y]
        board[empty_square_x - 1][empty_square_y] = BLANK_STATE
        empty_x = empty_square_x - 1
    else:
        return empty_x, empty_y
    return empty_x, empty_y


def main():
    board = generate_board()
    populate_board(board)
    print_board(board)
    empty_square_x, empty_square_y = find_empty_square(board)
    randomize(board, generate_random_string(), empty_square_x, empty_square_y)
    while True:
        direction = input_and_border_check(empty_square_x, empty_square_y)
        empty_square_x, empty_square_y = move(board, direction, empty_square_x, empty_square_y)
        print_board(board)


if __name__ == '__main__':
    main()


"""Move да приема само direction string и ако е грешен, да не го изпълнява, 
така когато randomize-ваме няма да имаме проблеми с boundary когато вкараме random стринг от asdwasdwasdwad..."""