import numpy as np 

## visualizing board
board = [["r", "n", "b", "q", "k", "b", "n", "r"],
         ["p", "p", "p", "p", "p", "p", "p", "p"],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         ["P", "P", "P", "P", "P", "P", "P", "P"],
         ["R", "N", "B", "Q", "K", "B", "N", "R"]]

encoded = {"R": 2 , "N": 3, "B": 4, "Q": 5, "K": 6, "P": 1, "r": -2, "n": -3, "b": -4, "q": -5, "k": -6, "p": -1, ".": 0}

## let's say we got an string as input and we need to convert into numerical board 
fen_string = "8/8/8/8/8/8/7q/7K w - - 0 1"

## convert fen string to board ["R", "N"] like that 
def fen_string_board(fen_string):  
    """will return exactly board pieces in a array"""
    rows = fen_string.split(" ")[0].split("/")
    board = []
    for row in rows:
        row_board = []
        for char in row:
            if char.isdigit():
                row_board.extend("." * int(char))
            else:
                row_board.append(char)
        board.append(row_board)
    return board

# board = fen_string_board(fen_string)
# print(board)

def get_turn(fen):
    """returning whose turn is next"""
    turn = fen.split(" ")[1]
    return turn

# print(get_turn(fen_string))

## view fen as a board style 
def to_view_fen_converted(board):
    """Printing fen string converted into board style"""
    for row in board:
        print(" ".join(row))

# print(to_view_fen_converted(board))

## now this will convert the board pieces to the numerical board representation 
def to_numericalboard(board, encoding):
    """Converting fen style board view to numerical_board representation"""
    moves = []
    for row in board:
        each_rows = []
        for c in row:
            each_rows.append(encoding.get(c, 0))
        moves.append(each_rows)
    
    return np.array(moves)

# print(to_numericalboard(board, encoded))