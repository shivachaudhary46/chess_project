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
        self.isWhiteTurn = True
        self.moveLog = []

class numericalBoard(gamestate):
    def __init__(self):
        '''
        i want to convert the string board to numerical board. so, we can do most of the 
        operations easily  
        '''



class Move:
    '''
        it will have the startSource and destination converted as row and columns
        maps key and values as rank to rows 
    '''
    rankToRows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    rankToCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v:k for k, v in rankToCols.items()}

    def __init__(self, startSq, endSq, board):
        ''' basically it will divide start source and ending destination (row, col) as seperate row and col'''
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceSource = board[self.startRow][self.startCol]
        self.pieceDest = board[self.endRow][self.endCol]

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

    def getRankColsTup(self, seq):
        ''' convert the sequences into tuples e4 to (3, 4)'''
        return self.rankToCols[seq[0]], self.rankToRows[seq[1]]
    
    def getChessNotationTup(self, seq):
        ''' return sequences as tuples e4e5 to (3, 4), (5, 6)'''
        source_move = self.getRankColsTup(seq[:2])
        dest_move = self.getRankColsTup(seq[2:])
        return source_move, dest_move 