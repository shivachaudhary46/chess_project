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
