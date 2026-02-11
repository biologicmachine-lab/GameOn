# GameOn

A complete, fully-functional chess game implementation in Python with move validation, check detection, and checkmate recognition.

## Features

- **Complete Chess Rules**: All piece movements (Pawn, Rook, Knight, Bishop, Queen, King)
- **Move Validation**: Prevents illegal moves and enforces chess rules
- **Check Detection**: Identifies when a king is in check
- **Checkmate Detection**: Recognizes game-ending conditions
- **Turn Management**: Enforces proper turn-taking between players
- **Capture Mechanics**: Properly handles piece captures
- **Algebraic Notation**: Uses standard chess notation (e.g., e2, e4)
- **Interactive CLI**: Play directly from the command line

## Installation

No external dependencies required! Just Python 3.6 or higher.

```bash
git clone https://github.com/biologicmachine-lab/GameOn.git
cd GameOn
```

## Usage

### Playing the Game

Run the chess game:

```bash
python3 chess.py
```

Enter moves using standard algebraic notation:
```
Enter move: e2 e4
```

Type `quit` to exit the game at any time.

### Running Tests

Run the comprehensive test suite:

```bash
python3 -m unittest test_chess -v
```

All 30 tests validate:
- Individual piece movement rules
- Board initialization and state management
- Turn switching and game flow
- Check and checkmate detection
- Complex game scenarios (including Scholar's Mate)

## Game Board

The board is displayed with standard chess notation:

```
  a b c d e f g h
  ---------------
8|BR BN BB BQ BK BB BN BR|8
7|BP BP BP BP BP BP BP BP|7
6|.  .  .  .  .  .  .  . |6
5|.  .  .  .  .  .  .  . |5
4|.  .  .  .  .  .  .  . |4
3|.  .  .  .  .  .  .  . |3
2|WP WP WP WP WP WP WP WP|2
1|WR WN WB WQ WK WB WN WR|1
  ---------------
  a b c d e f g h
```

Piece notation:
- **W** = White, **B** = Black
- **P** = Pawn, **R** = Rook, **N** = Knight
- **B** = Bishop, **Q** = Queen, **K** = King

## Code Structure

- `chess.py`: Main game implementation
  - `Piece` classes: Base and specialized piece classes with movement logic
  - `ChessBoard`: Board state and game rules enforcement
  - `ChessGame`: Game interface and user interaction
- `test_chess.py`: Comprehensive unit tests

## Example Game

```bash
$ python3 chess.py
Welcome to Chess!
Enter moves in format: e2 e4
Type 'quit' to exit

  a b c d e f g h
  ---------------
8|BR BN BB BQ BK BB BN BR|8
7|BP BP BP BP BP BP BP BP|7
6|.  .  .  .  .  .  .  . |6
5|.  .  .  .  .  .  .  . |5
4|.  .  .  .  .  .  .  . |4
3|.  .  .  .  .  .  .  . |3
2|WP WP WP WP WP WP WP WP|2
1|WR WN WB WQ WK WB WN WR|1
  ---------------
  a b c d e f g h

Current turn: white
Enter move: e2 e4
✓ Move successful
```

## License

MIT License - See LICENSE file for details

## Author

biologicmachine-lab
