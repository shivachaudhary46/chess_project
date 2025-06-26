import chess 
import chess.pgn


board = chess.Board()

# print(board)

# print(board.legal_moves)

# white 
# board.push_san("e4")

# # black
# board.push_san("e5")

# # white 
# board.push_san("Qh5")

# # black
# board.push_san("Nc6")

# # white
# board.push_san("Bc4")

# # black 
# board.push_san("Nf6")

# # white 
# board.push_san("Qxf7")

# # check mate
# print("checkmate state", board.is_checkmate())
# print(board)

legal_moves = board.legal_moves
# print("legal moves : ", list(legal_moves))

move = chess.Move.from_uci('g1f3')
if move in legal_moves:
    board.push_san('g1f3')

print(board)
print('---------------')
move = chess.Move.from_uci('b8c6')
if move in legal_moves:
    board.push_san('b8c6')

print(board)

print(f"is check position: {board.is_check()}")

fen = board.fen()
print(fen)

## how can you export from the fen style to the pgn headers
board2 = chess.Board(fen)
print(board2)

game = chess.pgn.Game()
game.headers["Event"] = "Test Game"
game.headers["Site"] = "Example.com"
game.headers["white"] = "Test player"
game.headers["black"] = "Test Opponent"

board = chess.Board()
game.setup(board)

exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
pgn_string = game.accept(exporter)
print("PGN game", pgn_string)