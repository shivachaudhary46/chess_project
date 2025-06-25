import chess 

board = chess.Board()

# print(board)

# print(board.legal_moves)

# white 
board.push_san("e4")

# black
board.push_san("e5")

# white 
board.push_san("Qh5")

# black
board.push_san("Nc6")

# white
board.push_san("Bc4")

# black 
board.push_san("Nf6")

# white 
board.push_san("Qxf7")

# check mate
print("checkmate state", board.is_checkmate())
print(board)