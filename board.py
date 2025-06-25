import numpy as np

encoded = {"R": 2, "N": 3, "B": 4, "Q": 5, "K": 6, "P": 1, "r": -2, "n": -3, "b": -4, "q": -5, "k":-6, "p": -1, ".": 0}

board= [["r", "n", "b", "k", "q", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "K", "Q", "B", "N", "R"]]

# numerical_board = np.array([[encoded[cell] for cell in row ]for row in board])
# print(numerical_board)

numerical_board1 = []
for row in board:
    each = []
    for i in row:
        each.append(encoded[i])
    numerical_board1.append(each)
    
numerical_board1=np.array(numerical_board1)
print(numerical_board1)

def knight_valid_moves(start_xy):
    directions = np.array([[-2, -1], [-2, 1], [2, -1], [1, 2]])
    all_move = []

    for direction in directions:
        move = start_xy + direction
        if 0 <= move[0] <= 7 and 0 <= move[1] <= 7 :
            all_move.append(move)
        else: 
            break
    
    all_move = np.array(all_move)
    return all_move

# knight_valid_moves((7, 6))

def queen_valid_moves(start_xy):
    directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]])
    all_move = []

    for direction in directions:
        for step in range(1, 8):
            move = start_xy + step * direction
            # print(move)
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                all_move.append(move)
            else: 
                break
     
    all_move = np.array(all_move)
    return all_move
# queen_move((2, 3))

def bishop_valid_moves(start_xy):
    directions = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
    all_move=[]
    for direction in directions:
        for step in range(1, 8):
            move=start_xy+step*direction
            if 0<=move[0]<=7 and 0<=move[1]<=7:
                all_move.append(move)
            else:
                break
    all_move=np.array(all_move)
    return all_move

# bishop_move((1, 2))

def rook_valid_moves(start_xy):
    directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    all_move=[]
    for direction in directions:
        for step in range(1, 8):
            move=start_xy+step*direction
            if 0<=move[0]<=7 and 0<=move[1]<=7:
                all_move.append(move)
            else:
                break
    all_move=np.array(all_move)
    return all_move

def king_valid_moves(start_xy):
    directions=np.array([[+1, 0], [-1, 0], [0, +1], [0, -1], [+1, +1], [-1, -1], [+1, -1], [-1, +1]])
    all_move=[]
    for direction in directions:
            move=start_xy+direction
            if 0<=move[0]<=7 and 0<=move[1]<7:
                all_move.append(move)
            else:
                break
    all_move=np.array(all_move)
    return all_move

def white_valid_pawn(board, start_xy):
    all_move = []
    row, col = start_xy
    # if one moves ahead 
    if row > 0 and board[row-1][col]==0:
        all_move.append(np.array([row-1, col]))
        # board[row-1][col]=board[row][col]

    ## if piece want to move two position at one time 
    if row == 6 and board[row-2][col]==0:
        all_move.append(np.array([row-2, col]))
        # board[row-2][col]=board[row][col]
    
    ## moving in diagnoal direction 
    for diag in [-1, +1]:
        new_row, new_col = row-1, diag+col
        if 0<=new_row<=7 and 0<=new_col<=7:
            if board[new_row][new_col] < 0:
                all_move.append(np.array([new_row, new_col]))

    all_move=np.array(all_move)
    return all_move

def black_valid_pawn(board, start_xy):
    moves = []
    row, col = start_xy
    ## moving one square each 
    if row < 7 and board[row+1][col] == 0:
        moves.append(np.array([row+1, col])) 

    if row == 1 and board[row+2][col] == 0:
        moves.append(np.array([row+2, col]))
    
    for diag in [-1, 1]:
        new_row, new_col = row+1, col+diag
        if 0 <= new_row <= 7 and 0 <= new_col <= 7:
            if board[new_row][new_col] > 0:
                moves.append(np.array([new_row, new_col]))

    return np.array(moves)

queen_list = queen_valid_moves((7, 4))
# print(queen_list)

numerical_board1[2][3] = 1
numerical_board1[2][5] = 4
print(numerical_board1)
white_pawn_list = white_valid_pawn(numerical_board1, (6, 4))
print(white_pawn_list)

black_pawn_list = black_valid_pawn(numerical_board1, (1, 4))
print(black_pawn_list)

