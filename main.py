from check_mate_detection import fen_string_board, to_view_fen_converted, get_turn, to_numericalboard, legal_move_generation, encoded
import numpy as np

# which will return the coordinatesn of PGN format in board
def square_to_index(square):
    files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    ranks = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

    file = square[0]
    rank = square[1]

    return ranks[rank], files[file]

## numerical to fen position basic one 
def numerical_to_fen(board):
    piece_map = {
        1: 'P', 2: 'R', 3: 'N', 4: 'B', 5: 'Q', 6: 'K',
        -1: 'p', -2: 'r', -3: 'n', -4: 'b', -5: 'q', -6: 'k',
        0: '0'
    }
    
    fen_rows = []
    for row in board:
        fen_row = ""
        empty_count = 0
        for cell in row:
            if cell == 0:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece_map[cell]
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    fen_position = '/'.join(fen_rows)
    return f"{fen_position} w KQkq - 0 1"

def parse_index(string):

    from_square = string[:2]
    to_square = string[2:]

    from_pos = square_to_index(from_square)
    to_pos = square_to_index(to_square)

    return from_pos, to_pos

string_index = parse_index("e4e5")
# print(string_index)

def make_move(board, from_pos, to_pos):
    new_board = board

    x, y = from_pos
    nx, ny = to_pos
    new_board[nx][ny] = board[x][y]
    new_board[x][y] = 0

    return new_board


def global_input():

    ## starting fen string 
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    ## white will get a starting turn 
    is_white = get_turn(fen) == "w"

    ## we can update this while loop 
    while True:

        ## first printing the board 
        board = fen_string_board(fen)
        to_view_fen_converted(board)

        ## then converting board to numerical board
        board=to_numericalboard(board, encoded)

        player = "white" if is_white else "black"

        take_input = input(f"{player} ! please insert a move like (e2e4, b1c3): ")

        try:
            ## coordinate of the input will come
            from_pos, to_pos = parse_index(take_input)

        except Exception as e:
            print("invalid input format!!, please enter like (e2de4)")
            continue # take input again 

        ## generate legal_moves for that move 
        legal_moves = legal_move_generation(board, fen, is_white)
            
        ## check player move is legal or not 
        if (from_pos, to_pos) in legal_moves:
            # board = make_move(board, (from_pos, to_pos))
            #. update fen accordingly 
            is_white = not is_white
            
        else:
            print("Illegal move! Please try again.")
            continue

        fen_string = numerical_to_fen(board)
        board = fen_string_board(fen_string)
        to_view_fen_converted(board)

'''
    create class which represents 8*8 visual board which is 2D numpy array 
'''
class chess:
    def __init__(self):
        self.board=np.array([["r", "n", "b", "q", "k", "b", "n", "r"],
                                ["p", "p", "p", "p", "p", "p", "p", "p"],
                                [".", ".", ".", ".", ".", ".", ".", "."],
                                [".", ".", ".", ".", ".", ".", ".", "."],
                                [".", ".", ".", ".", ".", ".", ".", "."],
                                [".", ".", ".", ".", ".", ".", ".", "."],
                                ["P", "P", "P", "P", "P", "P", "P", "P"],
                                ["R", "N", "B", "Q", "K", "B", "N", "R"]])
        self.isWhiteTurn=True
        
                                

if __name__ == "__main__":
    # global_input()
    pass