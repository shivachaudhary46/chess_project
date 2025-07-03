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

        take_input = input("enter a valid chess move: ").lower()
        print()

        '''we have board like wR, wB, wN but do we need to convert into the numerical array??'''
        validMoves=gs.getValidKingChecks()

        if len(validMoves) == 0:
            if not gs.isWhiteTurn :
                print("White won Game!!! \ncongratulation!!!")
                break
            else:
                print("Black won Game!!! \ncongratulation!!!")
                break

        if take_input == 'q' or take_input == 'exit':
            break
        
        if len(take_input) != 4:
            print("invalid input, please enter a move like e2e4")
            continue

        ''' if take_input like e4e5 then we have to convert it into tuples'''
        try:
            conversion = chessEngine1.Conversion(take_input)
            source, dest = conversion.getChessNotationTup()
            # print(source, dest)
        
            ''' now we have tuples (3, 4), (5, 6) now we can move in any direction first if we want to valid 
                later on then we can do by generate legal valid move generation '''
            move = chessEngine1.Move(source, dest, gs.board)
            
            if gs.isPlayerValidMove(move, validMoves):
                ''' now make the move '''
                gs.makeMove(move)
                
                '''print board condition'''
                gs.printBoardState()

            '''undoing a move'''
            if take_input == 'z' or take_input == 'undo':
                gs.undoMove()
                gs.printBoardState()
        
        except KeyError:
            print("Invalid square input. use coordinates like e2e4")

        except Exception as e:
            print(f"Error: {e}")
                
if __name__ == "__main__":
    main()
            
