"""
Unit tests for the chess game implementation.
"""

import unittest
from chess import (
    Piece, Pawn, Rook, Knight, Bishop, Queen, King,
    ChessBoard, ChessGame
)


class TestPieces(unittest.TestCase):
    """Test individual chess pieces."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
    
    def test_pawn_forward_move(self):
        """Test pawn can move forward one square."""
        pawn = Pawn('white', (6, 4))
        self.board[6][4] = pawn
        self.assertTrue(pawn.is_valid_move(self.board, (5, 4)))
    
    def test_pawn_double_move(self):
        """Test pawn can move forward two squares from starting position."""
        pawn = Pawn('white', (6, 4))
        self.board[6][4] = pawn
        self.assertTrue(pawn.is_valid_move(self.board, (4, 4)))
    
    def test_pawn_cannot_double_move_after_first_move(self):
        """Test pawn cannot move two squares after first move."""
        pawn = Pawn('white', (6, 4))
        pawn.has_moved = True
        self.board[6][4] = pawn
        self.assertFalse(pawn.is_valid_move(self.board, (4, 4)))
    
    def test_pawn_diagonal_capture(self):
        """Test pawn can capture diagonally."""
        white_pawn = Pawn('white', (6, 4))
        black_pawn = Pawn('black', (5, 5))
        self.board[6][4] = white_pawn
        self.board[5][5] = black_pawn
        self.assertTrue(white_pawn.is_valid_move(self.board, (5, 5)))
    
    def test_pawn_cannot_capture_forward(self):
        """Test pawn cannot capture directly forward."""
        white_pawn = Pawn('white', (6, 4))
        black_pawn = Pawn('black', (5, 4))
        self.board[6][4] = white_pawn
        self.board[5][4] = black_pawn
        self.assertFalse(white_pawn.is_valid_move(self.board, (5, 4)))
    
    def test_rook_horizontal_move(self):
        """Test rook can move horizontally."""
        rook = Rook('white', (7, 0))
        self.board[7][0] = rook
        self.assertTrue(rook.is_valid_move(self.board, (7, 5)))
    
    def test_rook_vertical_move(self):
        """Test rook can move vertically."""
        rook = Rook('white', (7, 0))
        self.board[7][0] = rook
        self.assertTrue(rook.is_valid_move(self.board, (3, 0)))
    
    def test_rook_cannot_jump(self):
        """Test rook cannot jump over pieces."""
        rook = Rook('white', (7, 0))
        blocking_piece = Pawn('white', (7, 2))
        self.board[7][0] = rook
        self.board[7][2] = blocking_piece
        self.assertFalse(rook.is_valid_move(self.board, (7, 5)))
    
    def test_knight_l_shape_move(self):
        """Test knight moves in L-shape."""
        knight = Knight('white', (7, 1))
        self.board[7][1] = knight
        self.assertTrue(knight.is_valid_move(self.board, (5, 2)))
        self.assertTrue(knight.is_valid_move(self.board, (5, 0)))
    
    def test_knight_can_jump(self):
        """Test knight can jump over pieces."""
        knight = Knight('white', (7, 1))
        blocking_piece = Pawn('white', (6, 1))
        self.board[7][1] = knight
        self.board[6][1] = blocking_piece
        self.assertTrue(knight.is_valid_move(self.board, (5, 2)))
    
    def test_bishop_diagonal_move(self):
        """Test bishop moves diagonally."""
        bishop = Bishop('white', (7, 2))
        self.board[7][2] = bishop
        self.assertTrue(bishop.is_valid_move(self.board, (4, 5)))
    
    def test_bishop_cannot_move_straight(self):
        """Test bishop cannot move in straight lines."""
        bishop = Bishop('white', (7, 2))
        self.board[7][2] = bishop
        self.assertFalse(bishop.is_valid_move(self.board, (7, 5)))
        self.assertFalse(bishop.is_valid_move(self.board, (4, 2)))
    
    def test_queen_moves_like_rook(self):
        """Test queen can move like a rook."""
        queen = Queen('white', (7, 3))
        self.board[7][3] = queen
        self.assertTrue(queen.is_valid_move(self.board, (7, 7)))
        self.assertTrue(queen.is_valid_move(self.board, (3, 3)))
    
    def test_queen_moves_like_bishop(self):
        """Test queen can move like a bishop."""
        queen = Queen('white', (7, 3))
        self.board[7][3] = queen
        self.assertTrue(queen.is_valid_move(self.board, (4, 6)))
    
    def test_king_one_square_move(self):
        """Test king can move one square in any direction."""
        king = King('white', (7, 4))
        self.board[7][4] = king
        self.assertTrue(king.is_valid_move(self.board, (7, 5)))
        self.assertTrue(king.is_valid_move(self.board, (6, 4)))
        self.assertTrue(king.is_valid_move(self.board, (6, 5)))
    
    def test_king_cannot_move_two_squares(self):
        """Test king cannot move two squares."""
        king = King('white', (7, 4))
        self.board[7][4] = king
        self.assertFalse(king.is_valid_move(self.board, (7, 6)))
        self.assertFalse(king.is_valid_move(self.board, (5, 4)))


class TestChessBoard(unittest.TestCase):
    """Test chess board functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.board = ChessBoard()
    
    def test_board_initialization(self):
        """Test board is initialized correctly."""
        # Check pawns
        for col in range(8):
            self.assertIsInstance(self.board.board[1][col], Pawn)
            self.assertEqual(self.board.board[1][col].color, 'black')
            self.assertIsInstance(self.board.board[6][col], Pawn)
            self.assertEqual(self.board.board[6][col].color, 'white')
        
        # Check rooks
        self.assertIsInstance(self.board.board[0][0], Rook)
        self.assertIsInstance(self.board.board[0][7], Rook)
        
        # Check knights
        self.assertIsInstance(self.board.board[0][1], Knight)
        self.assertIsInstance(self.board.board[0][6], Knight)
        
        # Check bishops
        self.assertIsInstance(self.board.board[0][2], Bishop)
        self.assertIsInstance(self.board.board[0][5], Bishop)
        
        # Check queens
        self.assertIsInstance(self.board.board[0][3], Queen)
        self.assertIsInstance(self.board.board[7][3], Queen)
        
        # Check kings
        self.assertIsInstance(self.board.board[0][4], King)
        self.assertIsInstance(self.board.board[7][4], King)
    
    def test_initial_turn(self):
        """Test white moves first."""
        self.assertEqual(self.board.current_turn, 'white')
    
    def test_valid_pawn_move(self):
        """Test a valid pawn move."""
        success, message = self.board.move_piece((6, 4), (4, 4))
        self.assertTrue(success)
        self.assertEqual(self.board.current_turn, 'black')
    
    def test_invalid_move_wrong_turn(self):
        """Test cannot move opponent's pieces."""
        success, message = self.board.move_piece((1, 4), (3, 4))
        self.assertFalse(success)
        self.assertIn("Not your turn", message)
    
    def test_invalid_move_no_piece(self):
        """Test cannot move from empty square."""
        success, message = self.board.move_piece((4, 4), (5, 4))
        self.assertFalse(success)
        self.assertIn("No piece", message)
    
    def test_turn_switching(self):
        """Test turns switch correctly."""
        self.board.move_piece((6, 4), (4, 4))
        self.assertEqual(self.board.current_turn, 'black')
        self.board.move_piece((1, 4), (3, 4))
        self.assertEqual(self.board.current_turn, 'white')
    
    def test_piece_capture(self):
        """Test piece can capture opponent's piece."""
        # Move white pawn forward
        self.board.move_piece((6, 4), (4, 4))
        # Move black pawn forward
        self.board.move_piece((1, 3), (3, 3))
        # Move white pawn to capture
        success, message = self.board.move_piece((4, 4), (3, 3))
        self.assertTrue(success)
        # Check that the black pawn is captured
        self.assertIsInstance(self.board.board[3][3], Pawn)
        self.assertEqual(self.board.board[3][3].color, 'white')
    
    def test_find_king(self):
        """Test finding king position."""
        white_king_pos = self.board.find_king('white')
        self.assertEqual(white_king_pos, (7, 4))
        black_king_pos = self.board.find_king('black')
        self.assertEqual(black_king_pos, (0, 4))
    
    def test_check_detection(self):
        """Test check detection."""
        # Clear some pieces to set up check scenario
        self.board.board[1][4] = None  # Remove black pawn in front of king
        self.board.board[6][4] = None  # Remove white pawn
        
        # Move white queen to check black king
        queen = self.board.board[7][3]
        self.board.board[7][3] = None
        self.board.board[1][3] = queen
        queen.position = (1, 3)
        
        self.assertTrue(self.board.is_in_check('black'))
        self.assertFalse(self.board.is_in_check('white'))
    
    def test_cannot_move_into_check(self):
        """Test cannot make a move that puts own king in check."""
        # Set up scenario where moving a piece would expose king
        self.board.board[6][4] = None  # Remove white pawn
        
        # Place white rook between white king and black queen
        self.board.board[5][4] = Rook('white', (5, 4))
        
        # Place black queen threatening king
        self.board.board[1][4] = None  # Remove black pawn
        black_queen = Queen('black', (1, 4))
        self.board.board[1][4] = black_queen
        
        self.board.current_turn = 'white'
        
        # Try to move rook away (would expose king to check)
        success, message = self.board.move_piece((5, 4), (5, 5))
        self.assertFalse(success)
        self.assertIn("check", message.lower())


class TestChessGame(unittest.TestCase):
    """Test chess game class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = ChessGame()
    
    def test_parse_position_valid(self):
        """Test parsing valid chess notation."""
        self.assertEqual(self.game.parse_position('e2'), (6, 4))
        self.assertEqual(self.game.parse_position('a1'), (7, 0))
        self.assertEqual(self.game.parse_position('h8'), (0, 7))
    
    def test_parse_position_invalid(self):
        """Test parsing invalid chess notation."""
        self.assertIsNone(self.game.parse_position('i9'))
        self.assertIsNone(self.game.parse_position('a0'))
        self.assertIsNone(self.game.parse_position('z5'))
        self.assertIsNone(self.game.parse_position('e'))
        self.assertIsNone(self.game.parse_position('ee2'))


class TestGameScenarios(unittest.TestCase):
    """Test complete game scenarios."""
    
    def test_scholars_mate_setup(self):
        """Test setting up Scholar's Mate (4-move checkmate)."""
        board = ChessBoard()
        
        # Move 1: White pawn e2-e4
        board.move_piece((6, 4), (4, 4))
        # Move 1: Black pawn e7-e5
        board.move_piece((1, 4), (3, 4))
        
        # Move 2: White bishop f1-c4
        board.move_piece((7, 5), (4, 2))
        # Move 2: Black knight b8-c6
        board.move_piece((0, 1), (2, 2))
        
        # Move 3: White queen d1-h5
        board.move_piece((7, 3), (3, 7))
        # Move 3: Black knight g8-f6
        board.move_piece((0, 6), (2, 5))
        
        # Move 4: White queen h5xf7# (checkmate)
        success, message = board.move_piece((3, 7), (1, 5))
        self.assertTrue(success)
        
        # Verify checkmate
        self.assertTrue(board.is_checkmate('black'))
    
    def test_stalemate_not_checkmate(self):
        """Test that stalemate is not detected as checkmate."""
        board = ChessBoard()
        
        # Clear board
        for row in range(8):
            for col in range(8):
                board.board[row][col] = None
        
        # Set up a simple position
        white_king = King('white', (7, 4))
        black_king = King('black', (0, 4))
        
        board.board[7][4] = white_king
        board.board[0][4] = black_king
        
        board.current_turn = 'white'
        
        # White is not in check, so not checkmate
        self.assertFalse(board.is_checkmate('white'))


if __name__ == '__main__':
    unittest.main()
