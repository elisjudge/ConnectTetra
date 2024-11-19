import numpy as np

from game.board import GameBoard
from game.player import Player

class ConnectTetra:
    def __init__(self, player1:Player, player2:Player, track_history:bool = False) -> None:
        if player1.symbol != 1 or player2.symbol != 2:
            raise ValueError("Players not initialized with correct symbols")
        self.gameboard = GameBoard()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.valid_moves = [col_index for col_index in range(self.gameboard.columns)]
        self.winner = None
        self.history = [] if track_history else None
        self.n_moves = 0

    def execute_move(self, player:Player, move):
        self.gameboard.board = (move, player.symbol)
        self.n_moves += 1

    def is_winner(self):
        for check_method in [
            self.is_4_in_a_row_horizontal,
            self.is_4_in_a_row_vertical,
            self.is_4_in_a_row_diag_left,
            self.is_4_in_a_row_diag_right,
        ]:
            result = check_method()
            if result:
                return result
        return 0

    def is_4_in_a_row_horizontal(self):
        for i in range((self.gameboard.rows - 1), -1, -1):
            l, r = 0, 1
            n_in_a_row = 0
            row = self.gameboard.board[i]

            if np.all(row == 0):
                break

            while l <= (self.gameboard.columns - 4):
                current_symbol = row[l]
                if current_symbol == 0:
                    n_in_a_row = 0
                    l = r
                    r = l+1
                elif current_symbol != 0:
                    n_in_a_row += 1
                    if n_in_a_row == 4:
                        return current_symbol
                    if current_symbol == row[r]:
                        r += 1
                    elif current_symbol != row[r]:
                        n_in_a_row = 0
                        l = r
                        r = l+1
        return 0

    def is_4_in_a_row_vertical(self):
        for i in range(self.gameboard.columns):
            l, r = 0, 1
            n_in_a_row = 0
            column = self.gameboard.board[:, i]

            if np.all(column == 0):
                continue

            while l <= (self.gameboard.rows - 4):
                current_symbol = column[l]
                if current_symbol == 0:
                    n_in_a_row = 0
                    l = r
                    r = l+1
                elif current_symbol != 0:
                    n_in_a_row += 1
                    if n_in_a_row == 4:
                        return current_symbol
                    if current_symbol == column[r]:
                        r += 1
                    elif current_symbol != column[r]:
                        n_in_a_row = 0
                        l = r
                        r = l+1
        return 0

    def is_4_in_a_row_diag_left(self):
        # Diagonal and above
        for i in range(self.gameboard.columns):
            l, r = 0, 1
            n_in_a_row = 0
            diag = np.diagonal(self.gameboard.board, offset=i)
            diag_len = len(diag)

            if diag_len < 4:
                break
            
            if np.all(diag == 0):
                continue

            while l <= (diag_len - 4):
                current_symbol = diag[l]
                if current_symbol == 0:
                    n_in_a_row = 0
                    l = r
                    r = l+1
                elif current_symbol != 0:
                    n_in_a_row += 1
                    if n_in_a_row == 4:
                        return current_symbol
                    if current_symbol == diag[r]:
                        r += 1
                    elif current_symbol != diag[r]:
                        n_in_a_row = 0
                        l = r
                        r = l+1
        
        # Below Diagonal
        for i in range(1, self.gameboard.columns):
            l, r = 0, 1
            n_in_a_row = 0
            diag = np.diagonal(self.gameboard.board, offset=-i)
            diag_len = len(diag)

            if diag_len < 4:
                break
            if np.all(diag == 0):
                continue

            while l <= (diag_len - 4):
                current_symbol = diag[l]
                if current_symbol == 0:
                    n_in_a_row = 0
                    l = r
                    r = l+1
                elif current_symbol != 0:
                    n_in_a_row += 1
                    if n_in_a_row == 4:
                        return current_symbol
                    if current_symbol == diag[r]:
                        r += 1
                    elif current_symbol != diag[r]:
                        n_in_a_row = 0
                        l = r
                        r = l+1
        return 0

    def is_4_in_a_row_diag_right(self):
        # Diagonal and above
        for i in range(self.gameboard.columns):
            l, r = 0, 1
            n_in_a_row = 0
            diag = np.fliplr(self.gameboard.board).diagonal(offset=i)
            diag_len = len(diag)

            if diag_len < 4:
                break
            
            if np.all(diag == 0):
                continue

            while l <= (diag_len - 4):
                current_symbol = diag[l]
                if current_symbol == 0:
                    n_in_a_row = 0
                    l = r
                    r = l+1
                elif current_symbol != 0:
                    n_in_a_row += 1
                    if n_in_a_row == 4:
                        return current_symbol
                    if current_symbol == diag[r]:
                        r += 1
                    elif current_symbol != diag[r]:
                        n_in_a_row = 0
                        l = r
                        r = l+1
        
        # Below Diagonal
        for i in range(1, self.gameboard.columns):
            l, r = 0, 1
            n_in_a_row = 0
            diag = np.fliplr(self.gameboard.board).diagonal(offset=-i)
            diag_len = len(diag)

            if diag_len < 4:
                break
            if np.all(diag == 0):
                continue

            while l <= (diag_len - 4):
                current_symbol = diag[l]
                if current_symbol == 0:
                    n_in_a_row = 0
                    l = r
                    r = l+1
                elif current_symbol != 0:
                    n_in_a_row += 1
                    if n_in_a_row == 4:
                        return current_symbol
                    if current_symbol == diag[r]:
                        r += 1
                    elif current_symbol != diag[r]:
                        n_in_a_row = 0
                        l = r
                        r = l+1
        return 0   

    def check_rows_columns_state(self, move):
        column_index = move
        if self.gameboard.is_column_full(column_index=column_index):
            self.gameboard.remove_column(column_index=column_index)
        
        elif self.gameboard.is_bottomrow_full():
            self.gameboard.remove_row()
            self.gameboard.add_row()
            self.gameboard.add_column()

    def update_valid_moves(self):
        self.valid_moves = [col_index for col_index in range(self.gameboard.columns)]

        if self.gameboard.columns == self.gameboard.MIN_COLS:
            for col_index in range(self.gameboard.columns):
                if self.gameboard.is_column_full(column_index=col_index):
                    self.valid_moves.remove(col_index)

    def switch_turns(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        elif self.current_player == self.player2:
            self.current_player = self.player1  

    def announce_winner(self):
        if self.player1.symbol == self.winner:
            print(f"{self.player1.name} won.")
        elif self.player2.symbol == self.winner:
            print(f"{self.player2.name} won.")
