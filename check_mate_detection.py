import numpy as np
### this page is full of the problem

directions = {
                "R": [[1, 0], [-1, 0], [0, 1], [0, -1]],
                "N": [[-2, -1], [-2, 1], [2, -1], [1, 2], [-1, 2], [2, 1], [-1, -2], [1, -2]], 
                "B": [[1, 1], [1, -1], [-1, 1], [-1, -1]], 
                "Q": [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]], 
                "K": [[+1, 0], [-1, 0], [0, +1], [0, -1], [+1, +1], [-1, -1], [+1, -1], [-1, +1]]
            }


encoded = {"R": 2 , "N": 3, "B": 4, "Q": 5, "K": 6, "P": 1, "r": -2, "n": -3, "b": -4, "q": -5, "k": -6, "p": -1, ".": 0}

def fen_string_board(fen_string):
    """will return exactly board positions in a array"""
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

def get_turn(fen):
    """returning whose turn is next"""
    turn = fen.split(" ")[1]
    return turn

def to_view_fen_converted(board):
    """Printing fen string converted into board style"""
    for row in board:
        print(" ".join(row))

## En passant 
def is_enpassant(board, fen_string, is_white):
    en_passant = fen_string.split(" ")[3]

    if en_passant == "-":
        ## there is no enpassant moves comming up next 
         return []   
    
    row_map = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    ep_col = col_map[en_passant[0]]
    ep_row = row_map[en_passant[1]]

    ## if white or black moves 2 square and it is side by side 
    ## then that situation is called enpassant 
    targets = []
    direction = -1 if is_white else 1
    
    for diag in [-1, +1]:
        nx, ny = ep_row + direction, ep_col + diag
        if 0<=nx<=7 and 0<=ny<=7:
            piece = board[nx][ny]
            if (is_white and piece==1) or (not is_white and piece == -1):
                targets.append(((ep_row, ep_col), (nx, ny)))
    return targets

## Legal move generation
## board will get all the fen string 


fen = "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
board = fen_string_board(fen)
board = to_numericalboard(board, encoded)
turn = get_turn(fen)
is_white = turn == "w"
# print(legal_move)
def encode_back_fen_legal_move(board, legal_move):

    row_encode = {0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1'}
    col_encode = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

    encoded_legal_moves = []
    for moves in legal_move:
        encode = "".join(col_encode[moves[1]]+row_encode[moves[0]])
        encoded_legal_moves.append(encode)

    return encoded_legal_moves

fen = "6k1/8/8/8/8/8/6Q1/7K w - - 0 1"
board = fen_string_board(fen)
board = to_numericalboard(board, encoded)

turn = get_turn(fen)
is_white = turn == "w"

fen = "6k1/8/8/8/8/8/6Q1/7K w - - 0 1"

