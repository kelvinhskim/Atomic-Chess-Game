# Author: Hyun Seok Kim
# GitHub username: kelvinhskim
# Date: 06/09/2024
# Description: The ChessVar class manages the state and logic of an Atomic Chess game,
# a variant of chess with special rules for capturing and explosions.
# The game follows standard chess rules for piece movements but introduces unique capture mechanics
# where captured pieces cause explosions that remove surrounding pieces except for pawns.
# The game ends when a king is captured or blown up.
#


class ChessVar:
    """
    Class to manage the game of Atomic Chess.

    Attributes:
        _game_board (list): A 2D list representing the 8x8 chess board.
        _current_player (str): The color of the player whose turn it is to move ('WHITE' or 'BLACK').
        _game_state (str): The current state of the game ('UNFINISHED', 'WHITE_WON', 'BLACK_WON').
    """

    def __init__(self):
        """
        Initializes the game with a new board and sets the initial game state and turn.
        """
        # Initialize the game board
        self._game_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        # Initialize other data members
        self._current_player = 'WHITE'
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """
        Returns the current state of the game.

        Returns:
            str: The current game state ('UNFINISHED', 'WHITE_WON', 'BLACK_WON').
        """
        return self._game_state

    def simulate_explosion(self, row, col):
        """
        Simulates an explosion to check if both kings would be destroyed.
        Args:
            row (int): The row index where the explosion starts.
            col (int): The column index where the explosion starts.
        Returns:
            bool: Returns True if only one or no king would be destroyed, False if both would be.
        """
        white_king_destroyed = False
        black_king_destroyed = False

        for r in range(max(0, row - 1), min(row + 2, 8)):
            for c in range(max(0, col - 1), min(col + 2, 8)):
                piece = self._game_board[r][c]
                if piece == 'K':
                    white_king_destroyed = True
                elif piece == 'k':
                    black_king_destroyed = True

        # If both kings are affected, return False to indicate the move is invalid
        return not (white_king_destroyed and black_king_destroyed)

    def make_move(self, start_square, end_square):
        """
        Attempts to make a move; returns True if successful, False otherwise.

        Checks if the game is unfinished and if it's the correct player's turn
        before attempting the move.

        Args:
            start_square (str): The starting position in algebraic notation, e.g., 'd2'.
            end_square (str): The destination position in algebraic notation, e.g., 'd4'.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self._game_state != 'UNFINISHED':
            return False

        # Convert algebraic notation to indices
        start_row, start_col = self.chess_notation_to_index(start_square)
        end_row, end_col = self.chess_notation_to_index(end_square)

        if not self.is_valid_move(start_row, start_col, end_row, end_col):
            return False

        moving_piece = self._game_board[start_row][start_col]
        captured_piece = self._game_board[end_row][end_col]

        # Temporarily execute the move
        self._game_board[start_row][start_col] = '.'
        self._game_board[end_row][end_col] = moving_piece

        # Check the explosion impact before finalizing the move
        if captured_piece != '.':
            if not self.simulate_explosion(end_row, end_col):
                # Revert the move if both kings would be destroyed
                self._game_board[start_row][start_col] = moving_piece
                self._game_board[end_row][end_col] = captured_piece
                return False
            # Apply the actual explosion if valid
            self.explode(end_row, end_col)

        # Update game state and switch player if the game continues
        self.update_game_state()
        if self._game_state == 'UNFINISHED':
            self._current_player = 'BLACK' if self._current_player == 'WHITE' else 'WHITE'
        return True

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """
        Checks if a move is valid.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The destination row index.
            end_col (int): The destination column index.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Check if the start position is within bounds
        if not (0 <= start_row < 8 and 0 <= start_col < 8):
            return False

        # Check if the end position is within bounds
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # Check if there is a piece at the start position
        piece = self._game_board[start_row][start_col]
        if piece == '.':
            return False

        # Check if the piece belongs to the current player
        if (piece.isupper() and self._current_player == 'BLACK') or (piece.islower()
                                                                     and self._current_player == 'WHITE'):

            return False

        # Check if the piece can move to the destination
        if piece.lower() == 'p':
            return self.is_valid_pawn_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == 'n':
            return self.is_valid_knight_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == 'b':
            return self.is_valid_bishop_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == 'r':
            return self.is_valid_rook_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == 'q':
            return self.is_valid_queen_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == 'k':
            return self.is_valid_king_move(start_row, start_col, end_row, end_col)

        return False

    def is_valid_pawn_move(self, start_row, start_col, end_row, end_col):
        """
        Checks if a pawn move is valid.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The destination row index.
            end_col (int): The destination column index.

        Returns:
            bool: True if the pawn move is valid, False otherwise.
        """
        piece = self._game_board[start_row][start_col]
        direction = 1 if piece.islower() else -1

        # Check for regular move
        if start_col == end_col and self._game_board[end_row][end_col] == '.':
            if start_row + direction == end_row:
                return True
            elif (start_row + 2 * direction == end_row and start_row in (1, 6)
                  and self._game_board[start_row + direction][start_col] == '.'):
                return True

        # Check for capturing move
        if abs(start_col - end_col) == 1 and start_row + direction == end_row:
            if (self._game_board[end_row][end_col] != '.' or self._current_player == 'WHITE'
                    and self._game_board[end_row][end_col].islower() or self._current_player == 'BLACK'
                    and self._game_board[end_row][end_col].isupper()):
                return True

        return False

    @staticmethod
    def is_valid_knight_move(start_row, start_col, end_row, end_col):
        """
        Checks if a knight move is valid.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The destination row index.
            end_col (int): The destination column index.

        Returns:
            bool: True if the knight move is valid, False otherwise.
        """
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def is_valid_bishop_move(self, start_row, start_col, end_row, end_col):
        """
        Checks if a bishop move is valid.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The destination row index.
            end_col (int): The destination column index.

        Returns:
            bool: True if the bishop move is valid, False otherwise.
        """
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1

        current_row, current_col = start_row + step_row, start_col + step_col
        while current_row != end_row and current_col != end_col:
            if self._game_board[current_row][current_col] != '.':
                return False
            current_row += step_row
            current_col += step_col

        return True

    def is_valid_rook_move(self, start_row, start_col, end_row, end_col):
        """
        Checks if a rook move is valid.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The destination row index.
            end_col (int): The destination column index.

        Returns:
            bool: True if the rook move is valid, False otherwise.
        """
        if start_row != end_row and start_col != end_col:
            return False

        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if self._game_board[start_row][col] != '.':
                    return False
        else:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if self._game_board[row][start_col] != '.':
                    return False

                    # Check the destination square for a valid capture
        destination_piece = self._game_board[end_row][end_col]
        if destination_piece != '.':
            if (destination_piece.isupper() and self._current_player == 'BLACK') or \
                    (destination_piece.islower() and self._current_player == 'WHITE'):
                return True
            else:
                return False  # Destination occupied by same color

        return True

    def is_valid_queen_move(self, start_row, start_col, end_row, end_col):
        """
        Checks if a queen move is valid.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The destination row index.
            end_col (int): The destination column index.

        Returns:
            bool: True if the queen move is valid, False otherwise.
        """
        return self.is_valid_bishop_move(start_row, start_col, end_row, end_col) or \
            self.is_valid_rook_move(start_row, start_col, end_row, end_col)

    def is_valid_king_move(self, start_row, start_col, end_row, end_col):
        """
        Checks if a king move is valid.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The destination row index.
            end_col (int): The destination column index.

        Returns:
            bool: True if the king move is valid, False otherwise.
        """
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if row_diff <= 1 and col_diff <= 1:
            # Ensure the destination is either empty or contains an opponent's piece
            dest_piece = self._game_board[end_row][end_col]
            return dest_piece == '.'
        return False

    @staticmethod
    def chess_notation_to_index(notation):
        """
        Converts chess notation to board indices.

        Args:
            notation (str): The chess notation (e.g., 'c3').

        Returns:
            tuple: A tuple containing the row and column indices.
        """
        column, row = notation
        return 8 - int(row), ord(column) - ord('a')

    def handle_explosion(self, row, col):
        """
        Handles the explosion effect when a piece is captured and ensures both kings are not destroyed simultaneously.

        Args:
            row (int): The row index of the captured piece.
            col (int): The column index of the captured piece.

        Returns:
            bool: True if the explosion is valid, False otherwise.
        """
        # Check if both kings are in the explosion radius
        white_king_destroyed = False
        black_king_destroyed = False

        for r in range(max(0, row - 1), min(row + 2, 8)):
            for c in range(max(0, col - 1), min(col + 2, 8)):
                if self._game_board[r][c] == 'K':
                    white_king_destroyed = True
                if self._game_board[r][c] == 'k':
                    black_king_destroyed = True

        # If both kings are destroyed, the move is invalid
        if white_king_destroyed and black_king_destroyed:
            return False

        # Otherwise, proceed with the explosion
        self.explode(row, col)
        return True

    def explode(self, row, col):
        """
        Handles the explosion effect when a piece is captured.
        Args:
            row (int): The row index of the captured piece.
            col (int): The column index of the captured piece.
        """
        # Track potential destruction of kings
        white_king_destroyed = False
        black_king_destroyed = False

        # Check each square in the explosion radius
        for r in range(max(0, row - 1), min(row + 2, 8)):
            for c in range(max(0, col - 1), min(col + 2, 8)):
                piece = self._game_board[r][c]
                if piece.lower() == 'k':
                    if piece == 'K':
                        white_king_destroyed = True
                    if piece == 'k':
                        black_king_destroyed = True

        # If both kings are destroyed, the move is invalid and should not proceed
        if white_king_destroyed and black_king_destroyed:
            return False

        # Apply explosion only if valid
        for r in range(max(0, row - 1), min(row + 2, 8)):
            for c in range(max(0, col - 1), min(col + 2, 8)):
                if self._game_board[r][c] != '.':
                    if self.is_king(self._game_board[r][c]):
                        if self._game_board[r][c] == 'K':
                            self._game_state = 'BLACK_WON'
                        else:
                            self._game_state = 'WHITE_WON'
                    self._game_board[r][c] = '.'

        return True

    @staticmethod
    def is_on_board(row, col):
        """
        Checks if a position is on the board.

        Args:
            row (int): The row index.
            col (int): The column index.

        Returns:
            bool: True if the position is on the board, False otherwise.
        """
        return 0 <= row < 8 and 0 <= col < 8

    def update_game_state(self):
        """
        Updates the game state after a move.
        """
        white_king, black_king = False, False

        for row in self._game_board:
            for piece in row:
                if piece == 'K':
                    white_king = True
                if piece == 'k':
                    black_king = True

        if not white_king:
            self._game_state = 'BLACK_WON'
        elif not black_king:
            self._game_state = 'WHITE_WON'

    @staticmethod
    def is_king(piece):
        """
        Checks if a piece is a king.

        Args:
            piece (str): The piece to check.

        Returns:
            bool: True if the piece is a king, False otherwise.
        """
        return piece.lower() == 'k'

    def print_board(self):
        """
        Prints the current state of the board.
        """
        for row in self._game_board:
            print(' '.join(row))
        print()


# game = ChessVar()
# print(game.make_move('d2', 'd4'))  # output True
# print(game.make_move('g7', 'g5'))  # output True
# print(game.make_move('c1', 'g5'))  # output True
# game.print_board()
# print(game.get_game_state())  # output UNFINISHED
