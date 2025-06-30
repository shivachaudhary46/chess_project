''' This file will be my main file '''
import chessEngine 
import pygame 
import chess 
import os

''' we can initalize the pygame '''
HEIGHT=WIDTH=512
DIMENSIONS=8 # since there are 8*8 field
SQ_SIZE = HEIGHT // 8
MAX_FPS=15
IMAGES={}

''' chess board top left is always light, and upper two rows are set
    for black pieces. so, basically we are going to load image file into dictionary
'''
def load_images():
    pieces=['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        IMAGES[piece]=pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
    '''NOTE: we can access the images by IMAGES[piece]'''

''' this is the main file which will show board and pieces '''
def main():
    pygame.init()
    screen=pygame.display.set_mode((HEIGHT, WIDTH))
    clock=pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    gs = chessEngine.gamestate()
    load_images()
    RUNNING = True
    sqSelected = () # no square initally, keep track of last click 
    playerClicks = [] # keep track of player clicks (two tuples: [(7, 4), (5, 6)])

    while RUNNING:
        # quit the event if the pygame get an quit request 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                RUNNING=False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                location=pygame.mouse.get_pos() #(x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                print(row, col)
                sqSelected = (row, col)
                if sqSelected == (row, col): # the user clicked the same square
                    sqSelected = () # deselector 
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd
                    print(playerClicks)
                
                if len(playerClicks) == 2: # after 2 are updated 
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs.board)
        clock.tick(MAX_FPS)
        # flip the result to display 
        pygame.display.flip()


''' This function is written to render board and pieces '''
def drawGameState(screen, gs):
    drawBoard(screen, gs)
    # we can also add feature like selecting pieces with cursor
    drawPieces(screen, gs)

'''Draw a chess board. usually the top left square is always light'''
def drawBoard(screen, gs):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            colors=[pygame.Color('white'), pygame.Color('light gray')]
            color=colors[((r+c)%2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
 
'''Drawing a chess pieces in a chess board'''
def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()

