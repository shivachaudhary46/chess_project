# Daily Progress Report

## DAY 5
Hello learner fellows !! i know that i have not write the daily report for the past 4 days but From, Today onwards i am starting to write. Today, ***Date: [2082-03-11]*** ***day: wednesday***

### Today's Goals
- [x] complete writing function from FEN style to Board notation
- [x] write an function to encode Board to numerical
- [x] Moves of each chess piece 

### Completed Tasks
1. Created a function that actually can help to write Board from FEN style
2. Completed writng function to encode the board style
3. Completed writing optimized function which will generate valid moves

### Code Snippets
```python
    def fen_string_board(fen_string):
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

    fen = "r1bq1rk1/ppp1bppp/2n2n2/3pp3/3PP3/2P1BN2/PP1N1PPP/R2QKB1R w KQ - 0 8"

    fen_board = fen_string_board(fen)

    for row in fen_board:
        print(" ".join(row))
```

### Challenges Faced
- I faced challange on while converting Board notation to numerical positions

### Solutions Found
- It was much easier , it just like that encoding from dictionary and pairing with keys and values

### Tomorrow's Plan
1. [ ] detecting checkmate
2. [ ] i also need to handle rules like (Castaling, En passant, Legal move generation considering game state, PGN/FEN parsing and saving games) 
3. [ ] Board Visualization and move legality checking 

## Progress Tracking:
1. I will be using GitHub Projects for task management and Notion for tracking

## Milestone Checklist:
- [x] Development environment setup
- [x] Basic board representation
- [ ] Move generation system
- [ ] Special moves implementation
- [ ] Game state management
- [ ] CLI interface
- [ ] Documentation
- [ ] Test suite
- [ ] Performance optimization
- [ ] Phase 1 completion

# Daily Progress Report

## DAY 6
Hello learner fellows! Back again for another update. ***Date: [2082-03-12]*** ***day: Thursday***

### Today's Goals
- [x] Start implementing checkmate detection
- [x] Begin handling special chess rules: Castling and En passant
- [x] Visualize the board and verify move legality

### Completed Tasks
1. Wrote the initial logic to detect checkmate positions on the board.
2. Started implementing the rules for Castling (kingside and queenside) and En passant.
3. Developed a simple board visualization using text output for easier move validation.
4. Refactored old code for better readability and added more comments for future reference.

### Code Snippets
```python
# Pseudocode for checkmate detection (simplified)
def is_checkmate(board, color):
    if is_in_check(board, color) and not has_any_legal_moves(board, color):
        return True
    return False

# Example board visualization
def display_board(board):
    for row in board:
        print(" ".join(row))

# Example usage
display_board(fen_board)
```

### Challenges Faced
- Understanding all the edge cases for checkmate situations and special moves (Castling, En passant).
- Making sure the move generation logic accounts for current game state and rules.

### Solutions Found
- Broke the problem into smaller functions—handling check, legal move generation, and special rules separately.
- Used test FEN positions and manual sketches to visualize tricky scenarios.

### Tomorrow's Plan
1. [ ] Finalize and test checkmate detection thoroughly.
2. [ ] Complete logic for Castling and En passant.
3. [ ] Work on PGN/FEN parsing and saving game progress.
4. [ ] Enhance board visualization for better UX.
