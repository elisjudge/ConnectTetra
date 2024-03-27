import numpy as np
import time
from game.connect_tetra import ConnectTetra
from ai.base_ai import BaseAI

def play_game():
    game = ConnectTetra(player1=BaseAI(name="Player1", symbol=1), player2=BaseAI(name="Player2", symbol=2))
    
    while game.n_moves <= 120:
        print(f"Number of Moves: {game.n_moves}")
        game.gameboard.display()
        current_state = game.gameboard.board
        current_move = game.current_player.select_move(valid_moves = game.valid_moves, state=current_state)

        game.history.append((np.copy(current_state), current_move, game.current_player))
        game.execute_move(game.current_player, current_move)

        game.winner = game.is_winner()
        if game.winner:
            game.announce_winner()
            game.gameboard.display()
            break
        
        game.check_rows_columns_state(move=current_move)
        game.winner = game.is_winner()
        if game.winner:
            game.announce_winner()
            game.gameboard.display()
            break

        game.update_valid_moves()
        game.switch_turns()
    
    if not game.winner:
        print("Game ended in Stalemate")
        game.gameboard.display()

    
def main():
    play_game()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print("Total Game time:", execution_time, "seconds")