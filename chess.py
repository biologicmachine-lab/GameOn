"""
Chess Game Implementation
A complete chess game with move validation and game state management.
"""

class Piece:
    """Base class for all chess pieces."""
    
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # tuple (row, col)
        self.has_moved = False
    
    def __repr__(self):
        return f"{self.color[0].upper()}{self.__class__.__name__[0]}"
    
    def is_valid_move(self, board, target):
        """Check if a move to target position is valid."""
        raise NotImplementedError("Subclasses must implement this method")


class Pawn(Piece):
    """Pawn piece."""
    
    def is_valid_move(self, board, target):
        row, col = self.position
        target_row, target_col = target
        direction = -1 if self.color == 'white' else 1
        
        # Forward move
        if col == target_col:
            if target_row == row + direction and board[target_row][target_col] is None:
                return True
            # Double move from starting position
            if not self.has_moved and target_row == row + 2 * direction:
                if board[row + direction][col] is None and board[target_row][target_col] is None:
                    return True
        
        # Diagonal capture
        if abs(target_col - col) == 1 and target_row == row + direction:
            target_piece = board[target_row][target_col]
            if target_piece and target_piece.color != self.color:
                return True
        
        return False


class Rook(Piece):
    """Rook piece."""
    
    def is_valid_move(self, board, target):
        row, col = self.position
        target_row, target_col = target
        
        # Must move in straight line
        if row != target_row and col != target_col:
            return False
        
        # Check path is clear
        if row == target_row:
            step = 1 if target_col > col else -1
            for c in range(col + step, target_col, step):
                if board[row][c] is not None:
                    return False
        else:
            step = 1 if target_row > row else -1
            for r in range(row + step, target_row, step):
                if board[r][col] is not None:
                    return False
        
        # Check target square
        target_piece = board[target_row][target_col]
        if target_piece is None or target_piece.color != self.color:
            return True
        
        return False


class Knight(Piece):
    """Knight piece."""
    
    def is_valid_move(self, board, target):
        row, col = self.position
        target_row, target_col = target
        
        # L-shaped move
        row_diff = abs(target_row - row)
        col_diff = abs(target_col - col)
        
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            target_piece = board[target_row][target_col]
            if target_piece is None or target_piece.color != self.color:
                return True
        
        return False


class Bishop(Piece):
    """Bishop piece."""
    
    def is_valid_move(self, board, target):
        row, col = self.position
        target_row, target_col = target
        
        # Must move diagonally
        if abs(target_row - row) != abs(target_col - col):
            return False
        
        # Check path is clear
        row_step = 1 if target_row > row else -1
        col_step = 1 if target_col > col else -1
        
        r, c = row + row_step, col + col_step
        while r != target_row:
            if board[r][c] is not None:
                return False
            r += row_step
            c += col_step
        
        # Check target square
        target_piece = board[target_row][target_col]
        if target_piece is None or target_piece.color != self.color:
            return True
        
        return False


class Queen(Piece):
    """Queen piece."""
    
    def is_valid_move(self, board, target):
        # Queen moves like rook or bishop
        row, col = self.position
        target_row, target_col = target
        
        # Check if it's a rook-like move
        if row == target_row or col == target_col:
            temp_rook = Rook(self.color, self.position)
            return temp_rook.is_valid_move(board, target)
        
        # Check if it's a bishop-like move
        if abs(target_row - row) == abs(target_col - col):
            temp_bishop = Bishop(self.color, self.position)
            return temp_bishop.is_valid_move(board, target)
        
        return False


class King(Piece):
    """King piece."""
    
    def is_valid_move(self, board, target):
        row, col = self.position
        target_row, target_col = target
        
        # Can move one square in any direction
        row_diff = abs(target_row - row)
        col_diff = abs(target_col - col)
        
        if row_diff <= 1 and col_diff <= 1:
            target_piece = board[target_row][target_col]
            if target_piece is None or target_piece.color != self.color:
                return True
        
        return False


class ChessBoard:
    """Chess board representation and game logic."""
    
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'white'
        self.move_history = []
        self.setup_board()
    
    def setup_board(self):
        """Initialize the chess board with pieces in starting positions."""
        # Set up pawns
        for col in range(8):
            self.board[1][col] = Pawn('black', (1, col))
            self.board[6][col] = Pawn('white', (6, col))
        
        # Set up other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(piece_order):
            self.board[0][col] = piece_class('black', (0, col))
            self.board[7][col] = piece_class('white', (7, col))
    
    def get_piece(self, position):
        """Get piece at position."""
        row, col = position
        return self.board[row][col]
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        
        if piece is None:
            return False, "No piece at source position"
        
        if piece.color != self.current_turn:
            return False, "Not your turn"
        
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False, "Target position out of bounds"
        
        if not piece.is_valid_move(self.board, to_pos):
            return False, "Invalid move for this piece"
        
        # Check if move would put own king in check
        if self.would_be_in_check(from_pos, to_pos):
            return False, "Move would put your king in check"
        
        # Execute move
        captured_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.position = to_pos
        piece.has_moved = True
        
        # Record move
        self.move_history.append({
            'from': from_pos,
            'to': to_pos,
            'piece': piece,
            'captured': captured_piece
        })
        
        # Switch turns
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        return True, "Move successful"
    
    def find_king(self, color):
        """Find the king of the specified color."""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None
    
    def is_square_under_attack(self, position, by_color):
        """Check if a square is under attack by pieces of the given color."""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == by_color:
                    if piece.is_valid_move(self.board, position):
                        return True
        return False
    
    def is_in_check(self, color):
        """Check if the king of the given color is in check."""
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        
        opponent_color = 'black' if color == 'white' else 'white'
        return self.is_square_under_attack(king_pos, opponent_color)
    
    def would_be_in_check(self, from_pos, to_pos):
        """Check if a move would put the current player's king in check."""
        # Make temporary move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        original_piece = self.board[to_row][to_col]
        original_position = piece.position
        
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.position = to_pos
        
        # Check if in check
        in_check = self.is_in_check(piece.color)
        
        # Restore board
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = original_piece
        piece.position = original_position
        
        return in_check
    
    def is_checkmate(self, color):
        """Check if the given color is in checkmate."""
        if not self.is_in_check(color):
            return False
        
        # Try all possible moves to see if any gets out of check
        for from_row in range(8):
            for from_col in range(8):
                piece = self.board[from_row][from_col]
                if piece and piece.color == color:
                    for to_row in range(8):
                        for to_col in range(8):
                            if piece.is_valid_move(self.board, (to_row, to_col)):
                                if not self.would_be_in_check((from_row, from_col), (to_row, to_col)):
                                    return False
        
        return True
    
    def display(self):
        """Display the chess board."""
        print("\n  a b c d e f g h")
        print("  ---------------")
        for row in range(8):
            print(f"{8-row}|", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    print(f"{str(piece)}", end=" ")
                else:
                    print(".", end=" ")
            print(f"|{8-row}")
        print("  ---------------")
        print("  a b c d e f g h\n")


class ChessGame:
    """Main chess game class."""
    
    def __init__(self):
        self.board = ChessBoard()
        self.game_over = False
    
    def parse_position(self, pos_str):
        """Convert chess notation (e.g., 'e2') to board coordinates."""
        if len(pos_str) != 2:
            return None
        
        if not pos_str[1].isdigit():
            return None
        
        col = ord(pos_str[0].lower()) - ord('a')
        row = 8 - int(pos_str[1])
        
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None
    
    def play(self):
        """Main game loop."""
        print("Welcome to Chess!")
        print("Enter moves in format: e2 e4")
        print("Type 'quit' to exit\n")
        
        while not self.game_over:
            self.board.display()
            print(f"Current turn: {self.board.current_turn}")
            
            # Check for checkmate
            if self.board.is_checkmate(self.board.current_turn):
                winner = 'black' if self.board.current_turn == 'white' else 'white'
                print(f"Checkmate! {winner.capitalize()} wins!")
                self.game_over = True
                break
            
            # Check for check
            if self.board.is_in_check(self.board.current_turn):
                print("Check!")
            
            # Get move input
            move_input = input("Enter move: ").strip().lower()
            
            if move_input == 'quit':
                print("Thanks for playing!")
                self.game_over = True
                break
            
            # Parse move
            parts = move_input.split()
            if len(parts) != 2:
                print("Invalid input format. Use: e2 e4")
                continue
            
            from_pos = self.parse_position(parts[0])
            to_pos = self.parse_position(parts[1])
            
            if from_pos is None or to_pos is None:
                print("Invalid position. Use format like 'e2' or 'a7'")
                continue
            
            # Attempt move
            success, message = self.board.move_piece(from_pos, to_pos)
            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")


if __name__ == "__main__":
    game = ChessGame()
    game.play()
