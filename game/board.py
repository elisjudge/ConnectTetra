import numpy as np
import random

class GameBoard():
    MAX_COLS = 10
    MIN_COLS = 5

    def __init__(self, rows=6, columns=7) -> None:
        self._rows = rows
        self._columns = columns
        self._board = np.full((rows, columns), 0)
        
        rand_n = random.random()
        if rand_n >= 0.5:
            self._add_end = True
        else:
            self._add_end = False

    def display(self):
        print(self._board)

    def add_column(self):
        if self._columns == GameBoard.MAX_COLS:
            return
        
        if self._add_end:
            self._board = np.insert(self._board, self._columns, 0, axis=1)
            self._columns += 1
            self._add_end = False
        else:
            self._board = np.insert(self._board, 0, 0, axis=1)
            self._columns += 1
            self._add_end = True

    def remove_column(self, column_index):
        if self._columns == GameBoard.MIN_COLS:
            return
        
        self._board = np.delete(self._board, column_index, axis=1)
        self._columns -= 1
                
    def remove_row(self):
        self._board = np.delete(self._board, -1, axis=0)
    
    def add_row(self):
        self._board = np.vstack((np.zeros(self._columns, dtype=int), self._board))

    def is_column_full(self, column_index):
        column = self._board[:, column_index]
        if np.all(column != 0):
            return True
        return False    

    def is_bottomrow_full(self):
        bottom_row = self._board[-1]
        if np.all(bottom_row != 0):
            return True
        return False    

    @property
    def rows(self):
        return self._rows
    
    @property
    def columns(self):
        return self._columns

    @property
    def board(self):
        return self._board
    
    @board.setter
    def board(self, move:tuple):
        column, token = move
        column_data = self._board[:, column]

        if np.all(column_data) != 0:
            raise Exception("You cannot make move here as column is full.") 
        
        for row in range(len(column_data) -1, -1, -1):
            if column_data[row] == 0:
                self._board[row, column] = token
                break 
