''' This is going to be main driver file where we are running logics '''

class gamestate:
    def __init__(self):
        '''
            Chess board is 8*8 2D array. each cell consist of  two CHAR
            where first CHAR represents (b , w) black or white of chess piece
            second CHAR represents (R, N, B, Q, K) 
            (--) represents empty cell 
        '''
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                    ['--', '--', '--', '--', '--', '--', '--', '--'],
                    ['--', '--', '--', '--', '--', '--', '--', '--'],
                    ['--', '--', '--', '--', '--', '--', '--', '--'],
                    ['--', '--', '--', '--', '--', '--', '--', '--'],
                    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                    ['wR', 'wN', 'wB', 'wQ', 'wK',  'wB', 'wN', 'wR']]
        self.directions = {
                "R": [[1, 0], [-1, 0], [0, 1], [0, -1]],
                "N": [[-2, -1], [-2, 1], [2, -1], [1, 2], [-1, 2], [2, 1], [-1, -2], [1, -2]], 
                "B": [[1, 1], [1, -1], [-1, 1], [-1, -1]], 
                "Q": [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]], 
                "K": [[+1, 0], [-1, 0], [0, +1], [0, -1], [+1, +1], [-1, -1], [+1, -1], [-1, +1]]
            }
        self.isWhiteTurn = True
        self.moveLog = []
        self.whiteKingPos = (7, 4)
        self.blackKingPos = (0, 4)
        self.checkMate = False  # one player does not have legal move for kings. 
        self.stalemate = False # both player does not have legal moves
        self.kingMoved = False
        self.rookMoved = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceSource
        self.moveLog.append(move) #log the move 
        self.isWhiteTurn = not self.isWhiteTurn
        if move.pieceSource == 'wK':
            self.whiteKingPos = (move.endRow, move.endCol)
        if move.pieceSource == 'bK':
            self.blackKingPos = (move.endRow, move.endCol)
         
    '''print a board state'''
    def printBoardState(self):
        print("   a  b  c  d  e  f  g  h")
        print()
        for i, row in enumerate(self.board):
            print(f'{8-i}  {" ".join(row)}  {8-i}')

        print()
        print("   a  b  c  d  e  f  g  h")

    '''undo moving the pieces'''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceSource
            self.board[move.endRow][move.endCol] = move.pieceDest
            self.isWhiteTurn = not self.isWhiteTurn
            if move.pieceSource == 'wK':
                self.whiteKingPos = (move.startRow, move.startCol)
            if move.pieceSource == 'bK':
                self.blackKingPos = (move.startRow, move.startCol)
            
    ''''''
    def getValidKingChecks(self):
        # generate all possible moves 
        moves = self.getAllValidMoves()
        # for each move, make the move
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            
            # going for opponent moves
            self.isWhiteTurn = not self.isWhiteTurn
            if self.inCheck():  # if they do attack the king then it is not valid move
                moves.remove(moves[i])

            self.isWhiteTurn = not self.isWhiteTurn
            self.undoMove()
        
        if self.inCheck():
            print(f"{"white" if self.isWhiteTurn else "Black"} king is in check condition")

        '''end the game check mate condition'''
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True

            else:
                self.checkMate = False
                self.staleMate = False       

        # generate all opponents move
        # for each of your opponent's moves, see if they attack your king 
        # if they do attack king then remove that move
        return moves
    
    '''determine if the king is under attacked or not ?'''
    def inCheck(self):
        if self.isWhiteTurn:
            return self.squareUnderAttack(self.whiteKingPos[0], self.whiteKingPos[1])
        else: 
            return self.squareUnderAttack(self.blackKingPos[0], self.blackKingPos[1])

    '''checks for if opponent moves is attacking a king pos??'''
    def squareUnderAttack(self, r, c):
        self.isWhiteTurn = not self.isWhiteTurn ## first switch for opponent moves
        oppo_moves = self.getAllValidMoves()
        self.isWhiteTurn = not self.isWhiteTurn ## bring back
        for move in oppo_moves:
            if move.endRow == r and move.endCol == c:
                return True
        return False


    '''generate all possible moves for each piece'''
    def getAllValidMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn == 'w' and self.isWhiteTurn) or (turn == 'b' and not self.isWhiteTurn):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(turn, r, c, moves)

                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)

                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)

                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)

                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)

                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        
        return moves

    '''get all pawn moves at a specific row and col in board state'''                                        
    def getPawnMoves(self, turn, r, c, moves):
        '''if white pawn then'''
        if self.isWhiteTurn:
            if r > 0 and self.board[r-1][c] == '--':
                moves.append(Move((r, c), (r-1, c), self.board))

            if r == 6 and self.board[r-2][c] == '--':
                moves.append(Move((r, c), (r-2, c), self.board))

            for diag in [-1, 1]:
                nx, ny = r - 1, c+diag
                if 0<=nx<=7 and 0<=ny<=7 :
                    target=self.board[nx][ny]
                    
                    if target[0] == 'b':
                        moves.append(Move((r, c), (nx, ny), self.board))
    
        if not self.isWhiteTurn:
            '''if black pawn then'''
            if r < 7 and self.board[r+1][c] == '--':
                moves.append(Move((r, c), (r+1, c), self.board))

            if r == 1 and self.board[r+2][c] == '--':
                moves.append(Move((r, c), (r+2, c), self.board))

            for diag in [-1, 1]:
                nx, ny = r + 1, c+diag
                if 0<=nx<=7 and 0<=ny<=7 :
                    target=self.board[nx][ny]
                    
                    if target[0] == 'w':
                        moves.append(Move((r, c), (nx, ny), self.board))

    '''get all knight moves at a specific row and col in board state'''
    def getKnightMoves(self, r, c, moves):
        for direction in self.directions['N']:
            nx, ny = r + direction[0], c + direction[1]
            if 0<=nx<=7 and 0<=ny<=7:
                target=self.board[nx][ny]
                if target == '--' or (target[0] == 'b' and self.isWhiteTurn) or (target[0] == 'w' and not self.isWhiteTurn):
                    moves.append(Move((r, c), (nx, ny), self.board))
    
    '''get all rook moves at a specific row and col in board state'''
    def getRookMoves(self, r, c, moves):
        for direction in self.directions['R']:
            for step in range(1, 8):
                nx, ny = r+step*direction[0], c+step*direction[1]
                
                ## the moving piece destination should be limit inside the 
                ## 8 * 8 array
                if 0<=nx<=7 and 0<=ny<=7:
                    target = self.board[nx][ny]

                    # if destination is empty 
                    if target == '--':
                        moves.append(Move((r, c), (nx, ny), self.board))

                    # capturing piece
                    elif ((target[0] == 'b' and self.isWhiteTurn) or (target[0] == 'w' and not self.isWhiteTurn)):
                        moves.append(Move((r, c), (nx, ny), self.board))
                        break
                    
                    ## target is same as one 
                    else:
                        break
                else:
                    break

    '''get all Queen moves at a specific row and col in board state'''
    def getQueenMoves(self, r, c, moves):
        enemyColor = 'b' if self.isWhiteTurn else 'w'
        for direction in self.directions['Q']:
            for step in range(1, 8):
                nx, ny = r+step*direction[0], c+step*direction[1]
                
                '''new row and new col must be inside 8*8 2D board visualization'''
                if 0<=nx<=7 and 0<=ny<=7:
                    target = self.board[nx][ny]

                    '''if destination is empty'''
                    if target == '--':
                        moves.append(Move((r, c), (nx, ny), self.board))

                    elif (target[0] == enemyColor):
                        '''How can i capture pieces ??'''
                        moves.append(Move((r, c), (nx, ny), self.board))
                        break
                    else:
                        '''Target same as the pieces'''
                        break
                else:
                    break
            

    '''get all king moves at a specific row and col'''
    def getKingMoves(self, r, c, moves):
        for direction in self.directions['K']:
            nx, ny = r + direction[0], c + direction[1]
            if 0<=nx<=7 and 0<=ny<=7:
                target=self.board[nx][ny]
                if target == '--' or (target[0] == 'b' and self.isWhiteTurn) or (target[0] == 'w' and not self.isWhiteTurn):
                    moves.append(Move((r, c), (nx, ny), self.board))

    '''get all bishop moves at a specific row and col'''
    def getBishopMoves(self, r, c, moves):
        for direction in self.directions['B']:
            for step in range(1, 8):
                nx, ny = r+step*direction[0], c+step*direction[1]
                
                ## the moving piece destination should be limit inside the 
                ## 8 * 8 array
                if 0<=nx<=7 and 0<=ny<=7:
                    target = self.board[nx][ny]

                    # if destination is empty 
                    if target == '--':
                        moves.append(Move((r, c), (nx, ny), self.board))

                    # capturing piece
                    elif ((target[0] == 'b' and self.isWhiteTurn) or (target[0] == 'w' and not self.isWhiteTurn)):
                        moves.append(Move((r, c), (nx, ny), self.board))
                        break
                    
                    ## target is same as one 
                    else:
                        break
                else:
                    break

    '''King side castaling of both white and black kings'''
    def canKingSideCastle(self, r, c, moves):
        if self.isWhiteTurn:
            # for white turn
            king_row, king_col = (7, 4)
            rook_row = 7
            castle_to_king_to = (7, 6)
            castle_rook_to = (7, 5)
            king_moved = self.kingMoved # True means king has moved
            rook_moved = self.rookMoved # again True means king has moved
        else:
            # for black turn 
            king_row, king_col = (0, 4)
            rook_row = 0
            castle_king_to = (0,6)
            castle_rook_to = (0,5)
            king_moved = self.kingMoved
            rook_moved = self.rookMoved

        # check 
        if not king_moved and not rook_moved :
            if (self.board[king_row][])

    '''king can castle'''
    def isKingCanCastle(self):
        # get a rook move 
        rook_valid_moves = self.getAllValidMoves()
        iterate_valid = []
        for each in rook_valid_moves:
            iterate_valid.append(((each.startRow, each.startCol), (each.endRow, each.endCol)))

        # check whose turn is now
        if self.isWhiteTurn: #white turn 

            if (7, 7) in rook_valid_moves and self.whitekingPos == (7, 4):
                return True
            
            return False
            
        else:
            if (0, 7) in rook_valid_moves and self.whiteKingPos == (0, 4):
                return True 
            
            return False 

    '''Queen side castaling of both white and black kings'''
    def isPlayerValidMove(self, move, validMoves):
        iterate_valid = []
        for each in validMoves:
            iterate_valid.append(((each.startRow, each.startCol), (each.endRow, each.endCol)))
        
        print(iterate_valid)
        source = move.startRow, move.startCol
        dest = move.endRow, move.endCol
        piece = (source, dest)
        return piece in iterate_valid
    

class numericalBoard(gamestate):

    ''' text format is encoded 
        later we have to convert to nnumerical board while doing the model training for chess Engine 
    '''
    encoded = {"wR": 2 , "wN": 3, "wB": 4, "wQ": 5, "wK": 6, "wP": 1, "bR": -2, "bN": -3, "bB": -4, "bQ": -5, "bK": -6, "bP": -1, "--": 0}
    def __init__(self):
        '''
        i want to convert the string board to numerical board. so, we can do most of the 
        operations easily  
        '''
        super().__init__()

    '''adding decorator so we don't have to add self argument '''
    @staticmethod 
    def to_numericalboard(board, encoding):
        ''' Chess has 2D array board view. so we convert numerical_board representation later on if 
        before creating a new model'''
        num_board = []
        for row in board:
            each_rows = []
            for c in row:
                each_rows.append(encoding.get(c, 0))
            num_board.append(each_rows)
        
        return num_board
    
    def get_numericalboard(self):
        return self.to_numericalboard(self.board, self.encoded)


class Move:
    '''
        it will have the startSource and destination converted as row and columns
        maps key and values as rank to rows 
    '''
    def __init__(self, startSq, endSq, board):
        ''' basically it will divide start source and ending destination (row, col) as seperate row and col'''
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceSource = board[self.startRow][self.startCol]
        self.pieceDest = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    '''
    prints like source to destination of pieces 
    '''
    def __str__(self):
        print(f"Move: {self.pieceSource} from ({self.startRow}, {self.startCol}) to ({self.endRow}, {self.endCol})")

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

'''
    it will have the startSource and destination converted as row and columns
    maps key and values as rank to rows 
'''
class Conversion:
    rankToRows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    rankToCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v:k for k, v in rankToCols.items()}

    def __init__(self, seq):
        self.seq = seq.lower()

    def getChessNotationSeq(self):
        '''
        it will return files like e4e5
        '''
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        '''
        basically, it will return the tuple(rows, cols) to files like e4
        '''
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def getRankColsTup(self, move):
        ''' convert the sequences into tuples e4 to (3, 4) '''
        file_char=move[0]
        rank_char=move[1]

        '''cause in 2D array we look first row and then col'''
        row, col = self.rankToRows[rank_char], self.rankToCols[file_char]
        return row, col
    
    def getChessNotationTup(self):
        ''' return sequences as tuples e4e5 to (3, 4), (5, 6) '''
        source_move = self.getRankColsTup(self.seq[:2])
        dest_move = self.getRankColsTup(self.seq[2:])
        return source_move, dest_move 
