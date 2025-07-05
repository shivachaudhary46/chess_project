import chessEngine1

'''Main driver of file'''
def main():
    gs = chessEngine1.gamestate()

    '''description for users'''
    print()
    print("******** Chess Game ********")
    print()
    print("created by 'shivah chaudhary'")
    print("enter a chess moves like (e2e4, b1c3, e7e8) \nenter (q, exit) for exit \nenter (z, undo) for undo: ")
    
    while True:
        '''show which turn (black, white)'''
        print(f"Turn: {'White' if gs.isWhiteTurn else 'Black'}")
        print()

        '''print board , without this so confusing '''
        gs.printBoardState()
        print()

        '''we have board like wR, wB, wN but do we need to convert into the numerical array??'''
        validMoves = gs.getValidKingChecks()

        if len(validMoves) == 0:
            if not gs.isWhiteTurn:
                print("White won Game!!! \ncongratulation!!!")
                break
            else:
                print("Black won Game!!! \ncongratulation!!!")
                break

        take_input = input("enter a valid chess move: ").lower()
        print()

        if take_input == 'q' or take_input == 'exit':
            break
        
        '''Handle undo move'''
        if take_input == 'z' or take_input == 'undo':
            gs.undoMove()
            continue
        
        if len(take_input) != 4:
            print("invalid input, please enter a move like e2e4")
            continue

        ''' if take_input like e4e5 then we have to convert it into tuples'''
        try:
            conversion = chessEngine1.Conversion(take_input)
            source, dest = conversion.getChessNotationTup()
            
            # move was generated from the valid moves 
            move = None
            for valid_move in validMoves:
                if (valid_move.startRow == source[0] and valid_move.startCol == source[1] and 
                    valid_move.endRow == dest[0] and valid_move.endCol == dest[1]):
                    move = valid_move
                    break
            
            if move:
                # print(f"Executing move: {move.pieceSource} with isCastle={move.isCastle}")
                gs.makeMove(move)
                # print("Move executed successfully!")
            else:
                print("Invalid move! Please try again.")
        
        except KeyError:
            print("Invalid square input. use coordinates like e2e4")

        except Exception as e:
            print(f"Error: {e}")
                
if __name__ == "__main__":
    main()