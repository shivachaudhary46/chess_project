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

def to_numericalboard(board, encoding):
    """Converting fen style board view to numerical_board representation"""
    moves = []
    for row in board:
        each_rows = []
        for c in row:
            each_rows.append(encoding.get(c, 0))
        moves.append(each_rows)
    
    return moves


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
                        moves.append(((x, y), (nx, ny)))

                    # capturing piece
                    elif ((target < 0 and not iswhite) or (target > 0 and iswhite)):
                        moves.append(((x, y), (nx, ny)))
                        break
                    
                    ## target is same as one 
                    else:
                        break
                else:
                    break
        return moves

    elif name in ["N", "K"]:
        for dx, dy in directions[name]:
            nx, ny= x+dx , y+dy
            if 0<=nx<=7 and 0<=ny<=7:
                target = board[nx][ny]
                if target == 0 or ((target < 0 and not iswhite) or (target > 0 and iswhite)):
                    moves.append(((x, y), (nx, ny)))
        return moves

    elif name == "P":
        if iswhite: ## black
            ## move one direction each 
            if x < 7 and board[x+1][y] == 0 :
                moves.append(((x, y), (x+1, y)))
            
            ## move two squares if row position is 1
            if x == 1 and board[x+2][y]:
                moves.append(((x, y), (x+2, y)))

            ## capture piece diagnoally
            for diag in [-1, 1]:
                nx, ny = x + 1, y + diag
                if 0<=nx<=7 and 0<=ny<=7: 
                    target = board[nx][ny]
                    if target > 0 :
                        moves.append(((x, y),(nx, ny)))
            
            return moves

        else:
            # for white pawn 
            if x > 0 and board[x-1][y] == 0 :
                moves.append(((x, y),(x-1, y)))
            
            ## move two squares if row position is 1
            if x == 6 and board[x-2][y]:
                moves.append(((x, y), (x-2, y)))

            ## capture piece diagnoally
            for diag in [-1, 1]:
                nx, ny = x + 1, y + diag
                if 0<=nx<=7 and 0<=ny<=7: 
                    target = board[nx][ny]
                    if target < 0 :
                        moves.append(((x, y),(nx, ny)))

            return moves
        

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
                targets.append(((ep_row, ep_col), (nx, ny)))
    return targets

## Legal move generation
## board will get all the fen string 
def legal_move_generation(board, fen_string, is_white):
    legal_moves = []
    
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

    # For white king on row 7
    if is_white and 6 in board[7]:
        king_start = (7, 4)

        if can_castle_kingside(board, fen_string, is_white):
            king_end = (7, 6)  # King goes from e1 to g1
            legal_moves.append((king_start, king_end))

        if can_castle_queenside(board, fen_string, is_white):
            king_end = (7, 2)  # King goes from e1 to c1
            legal_moves.append((king_start, king_end))

    # For black king on row 0
    if not is_white and 6 in board[0]:
        king_start = (0, 4)

        if can_castle_kingside(board, fen_string, is_white):
            king_end = (0, 6)  # e8 to g8
            legal_moves.append((king_start, king_end))

        if can_castle_queenside(board, fen_string, is_white):
            king_end = (0, 2)  # e8 to c8
            legal_moves.append((king_start, king_end))

    enp_moves = is_enpassant(board, fen_string, is_white)
    for x, y, enp_rows, enp_cols in enp_moves:
        legal_moves.append(((x, y), (enp_rows, enp_cols)))

    return legal_moves

fen = "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
board = fen_string_board(fen)
board = to_numericalboard(board, encoded)
turn = get_turn(fen)
is_white = turn == "w"
legal_move = legal_move_generation(board, fen, is_white)
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
# print(board)
# print(find_king(board, False))
print(board)
def find_king(board, is_white):
    
    for x in range(0, 8):
        for y in range(0, 8):
            if is_white and board[x][y] == 6:
                return (x, y)

            if not is_white and board[x][y] == -6:
                return (x, y)

def is_check(board, is_white):

    king_position = find_king(board, is_white)

    opponent_color = not is_white

    opponent_moves = legal_move_generation(board, fen, opponent_color)
    ## king has not moved 

    for each in opponent_moves:
        if king_position in each:
            return True
        
    return False

# def make_move(board, move):
#     new_board = np.copy(board)
#     from_x, from_y =. 
    
## now going for the chess check_mate conditions 
# def is_check_mate(board, is_white):

#     ## if board has no check condition then there will never checkmate conditions either
#     if not is_check(board, is_white):
#         return False
    
#     ## if the oponent is giving check then king can escape check?? 

#     own_moves = legal_move_generation(board, fen, is_white)
#     for move in own_moves:
        
#         from_x, from_y = move[0]
#         to_x, to_y = move[1]

#         print(from_x, from_y, to_x,  to_y)
        # new_board = np.copy(board)
        
        # move = make_move()
        # if not is_check(new_board, is_white):
        #     return False

def square_to_index(square):
    files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    ranks = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

    file = square[0]
    rank = square[1]

    return ranks[rank], files[file]

def parse_index(string):

    from_square = string[:2]
    to_square = string[2:]

    from_pos = square_to_index(from_square)
    to_pos = square_to_index(to_square)

    return from_pos, to_pos

string_index = parse_index("e4e5")
# print(string_index)

def global_input():

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    is_white = get_turn(fen) == "w"

    while True:

        ## printing the board 
        board = fen_string_board(fen)
        to_view_fen_converted(board)
        board=to_numericalboard(board, encoded)

        player = "white" if is_white else "black"

        take_input = input(f"{player} ! please insert a move like (e2e4, b1c3): ")

        try:
            from_pos, to_pos = parse_index(take_input)
        except Exception as e:
            print("Invalid input format!!")

        ## generate legal_moves 
        legal_moves = legal_move_generation(board, fen, is_white)
        print(legal_moves)
        ## check player move is legal 


global_input()


turn = get_turn(fen)
is_white = turn == "w"
# print(is_check(board, is_white))
# print(is_check_mate(board, is_white))
# is_check_mate(board, is_white)


    ## if black king exist in the any type of routes 
        # moves by white piece
        # then that scenario is check 

        ## and same scenario for the white king as. well 

        ## what is checkmate condition :
        ## check mate is a condition where king cannot move in any
        ## of the direction if it is attacked.

fen = "6k1/8/8/8/8/8/6Q1/7K w - - 0 1"


turn = get_turn(fen)
is_white = turn == "w"
board = fen_string_board(fen)
board = to_numericalboard(board, encoded)
# print(board)

check = is_check(board, is_white)
# print(check)
