import numpy as np

encoded = {"R": 2 , "N": 3, "B": 4, "Q": 5, "K": 6, "P": 1, "r": -2, "n": -3, "b": -4, "q": -5, "k": -6, "p": -1, ".": 0}
fen = "r1bq1rk1/ppp1bppp/2n2n2/3pp3/3PP3/2P1BN2/PP1N1PPP/R2QKB1R w KQ - 0 8"

directions = {
                "R": [[1, 0], [-1, 0], [0, 1], [0, -1]],
                "N": [[-2, -1], [-2, 1], [2, -1], [1, 2], [-1, 2], [2, 1], [-1, -2], [1, -2]], 
                "B": [[1, 1], [1, -1], [-1, 1], [-1, -1]], 
                "Q": [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]], 
                "K": [[+1, 0], [-1, 0], [0, +1], [0, -1], [+1, +1], [-1, -1], [+1, -1], [-1, +1]]
            }

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
    turn = fen.split(' ')[1]
    return turn

def to_view_fen_converted(board):
    """Printing fen string converted into board style"""
    for row in board:
        print(" ".join(row))

def to_numericalboard(board, encoding):
    """Converting fen style board view to numerical_board representation"""
    moves = []
    for row in board:
        each_rows = []
        for c in row:
            each_rows.append(encoding.get(c, 0))
        moves.append(each_rows)
    
    return np.array(moves)

def can_castle_kingside(board,  fen_string, is_white):
    """Return False and true when king (white or black) piece cannot castle / can castle"""
 
    castling_rights = fen_string.split(" ")[2]

    ## before castling important thing is that the current fen style must
    ## have K or k should be inlcluded. 
    if  is_white and "K" not in castling_rights:
        return False
    if not is_white and "k" not in castling_rights:
        return False
    
    ## this statement makes clear which row to go for 
    ## when white piece has turn and viceversa 
    row = 7 if is_white else 0 

    ## the two squares (7, 5), (7, 6) must be empty to castle
    if board[row][5] != 0  and board[row][6] != 0:
        return False
    return True

def can_castle_queenside(board, fen_string, is_white):
    """Return False and true when Queen (white or black) piece cannot castle / can castle"""
    castling_rights = fen_string.split(" ")[2]

    if is_white and "Q" not in castling_rights:
        return False
    if not is_white and "q" not in castling_rights:
        return False
    
    ## this statement makes clear which row to go for 
    ## when white piece has turn and viceversa 
    row = 7 if is_white else 0

    if board[row][1] != 0 or board[row][2] != 0 or board[row][3] != 0:
        return False
    return True 

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
                targets.append((nx, ny, ep_row, ep_col))
    return targets

fen = "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"

board = fen_string_board(fen)
board = to_numericalboard(board, encoded)

# print(board)

###. finding legal moves
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

## Legal move generation
## board will get all the fen string 
def legal_move_generation(board, fen_string):
    legal_moves = []
    is_white = get_turn(fen_string) == "w"
    
    for x in range(8):
        for y in range(8):

            piece_code = board[x][y]

            # skip empty squares 
            if piece_code == 0:
                continue

            ## skip opponent pieces 
            if (is_white and piece_code < 0) or (not is_white and piece_code > 0):
                continue

            piece_letter = list(encoded.keys())[list(encoded.values()).index(piece_code)]
            moves = all_valid_moves(piece_letter, (x, y), board)
            for move in moves :
                legal_moves.append(move)

    if is_white and 6 in board[7]:
        if can_castle_kingside(board, fen_string, is_white):
            legal_moves.append("white can castle king side")
        if can_castle_queenside(board, fen_string, is_white):
            legal_moves.append("white can castle queen side")   
    if not is_white and 6 in board[0]:
        if can_castle_kingside(board, fen_string, is_white):
            legal_moves.append("black can castle king side")
        if can_castle_queenside(board, fen_string, is_white):
            legal_moves.append("black can castle queen side")

    enp_moves = is_enpassant(board, fen_string, is_white)
    for x, y, enp_rows, enp_cols in enp_moves:
        legal_moves.append(((x, y), (enp_rows), (enp_cols), 'en_passant'))

    return legal_moves

fen = "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
board = fen_string_board(fen)
board = to_numericalboard(board, encoded)
print(legal_move_generation(board, fen))


# print(list(encoded.keys())[list(encoded.values()).index(board[7][0])])


## game state whose turn is now 

## basically the user will give use a PGN formate 
# then we need to convert it to fen and
# update board condition 
