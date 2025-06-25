import numpy as np 

board = [["r", "n", "b", "q", "k", "b", "n", "r"],
                   ["p", "p", "p", "p", "p", "p", "p", "p"],
                   [".", ".", ".", ".", ".", ".", ".", "."],
                   [".", ".", ".", ".", ".", ".", ".", "."],
                   [".", ".", ".", ".", ".", ".", ".", "."],
                   [".", ".", ".", ".", ".", ".", ".", "."],
                   ["P", "P", "P", "P", "P", "P", "P", "P"],
                   ["R", "N", "B", "Q", "K", "B", "N", "R"]]

encoded = {"R": 2 , "N": 3, "B": 4, "Q": 5, "K": 6, "P": 1, "r": -2, "n": -3, "b": -4, "q": -5, "k": -6, "p": -1, ".": 0}

## store the numerical reprsentation
numerical_representation = []
for row in board:
    each=[]
    for i in row: 
        each.append(encoded[i])
    numerical_representation.append(each)

num_board =np.array(numerical_representation)
# print(np.array(numerical_representation))
        
directions = {
                "R": [[1, 0], [-1, 0], [0, 1], [0, -1]],
                "N": [[-2, -1], [-2, 1], [2, -1], [1, 2], [-1, 2], [2, 1], [-1, -2], [1, -2]], 
                "B": [[1, 1], [1, -1], [-1, 1], [-1, -1]], 
                "Q": [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]], 
                "K": [[+1, 0], [-1, 0], [0, +1], [0, -1], [+1, +1], [-1, -1], [+1, -1], [-1, +1]]
            }
# print(num_board)

## class piece for showing position and piece
class chess_piece:
    def __init__(self, piece, position):
        self.piece = piece ## this is the piece 
        self.position = position ## tuples

    def is_white(self, piece, board):
        x, y = self.position
        if board[x][y] == piece:
            ## position matches with piece
            if piece > 0:
                return True
            else:
                return False
            
## chess piece knowing 
piece = chess_piece("Q", (7, 3))
# print(piece.piece)
# print(piece.position)
# print(piece.is_white(5, num_board))
## converting the fen style to board
def fen_string_board(fen_string):
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

fen = "r1bq1rk1/ppp1bppp/2n2n2/3pp3/3PP3/2P1BN2/PP1N1PPP/R2QKB1R w KQ - 0 8"

fen_board = fen_string_board(fen)

for row in fen_board:
    print(" ".join(row))

def to_numericalboard(board, encoding):
    return np.array([[encoding.get(cell, 0) for cell in row] for row in board])

board = to_numericalboard(fen_board, encoded)
print(board)

def all_valid_moves(piece, start_pos, board):
    x, y = start_pos
    name = piece.upper()
    piece_code = encoded[piece]
    iswhite = piece_code < 0
    moves = []
    
    if name in ["R", "B", "Q"]:
        for direction in directions[name]:
            for step in range(1, 8):
                nx, ny = x+step*direction[0], y+step*direction[1]
                
                ## the moving piece destination should be limit inside the 
                ## 8 * 8 array
                if 0<=nx<=7 and 0<=ny<=7:
                    target = board[nx][ny]

                    # if destination is empty 
                    if target == 0:
                        moves.append(np.array([nx, ny]))

                    # capturing piece
                    elif ((target < 0 and not iswhite) or (target > 0 and iswhite)):
                        moves.append(np.array([nx, ny]))
                        break
                    
                    ## target is same as one 
                    else:
                        break
                else:
                    break
        return np.array(moves)

    elif name in ["N", "K"]:
        for dx, dy in directions[name]:
            nx, ny= x+dx , y+dy
            if 0<=nx<=7 and 0<=ny<=7:
                target = board[nx][ny]
                if target == 0 or ((target < 0 and not iswhite) or (target > 0 and iswhite)):
                    moves.append((nx, ny))
        return np.array(moves)

    elif name == "P":
        if iswhite: ## black
            ## move one direction each 
            if x < 7 and board[x+1][y] == 0 :
                moves.append((x+1, y))
            
            ## move two squares if row position is 1
            if x == 1 and board[x+2][y]:
                moves.append((x+2, y))

            ## capture piece diagnoally
            for diag in [-1, 1]:
                nx, ny = x + 1, y + diag
                if 0<=nx<=7 and 0<=ny<=7: 
                    target = board[nx][ny]
                    if target > 0 :
                        moves.append((nx, ny))
            
            return moves

        else:
            # for white pawn 
            if x > 0 and board[x-1][y] == 0 :
                moves.append((x-1, y))
            
            ## move two squares if row position is 1
            if x == 6 and board[x-2][y]:
                moves.append((x-2, y))

            ## capture piece diagnoally
            for diag in [-1, 1]:
                nx, ny = x + 1, y + diag
                if 0<=nx<=7 and 0<=ny<=7: 
                    target = board[nx][ny]
                    if target < 0 :
                        moves.append((nx, ny))

            return moves


# num_board[3][5] = 6
# print(num_board)
# valid_move = all_valid_moves("P", (6, 0), num_board)
# print(valid_move)
    

