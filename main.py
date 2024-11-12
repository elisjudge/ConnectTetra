import numpy as np
from game.connect_tetra import ConnectTetra
from ai.base_ai import BaseAI
from utils.utils import timeit, profiler

def play_game():
    game = ConnectTetra(player1=BaseAI(name="Player1", symbol=1), player2=BaseAI(name="Player2", symbol=2))
    
    while game.n_moves <= 120:
        
        current_state = game.gameboard.board
        current_move = game.current_player.select_move(valid_moves = game.valid_moves, state=current_state)

        game.history.append((np.copy(current_state), current_move, game.current_player))
        game.execute_move(game.current_player, current_move)

        game.winner = game.is_winner()
        if game.winner:
            game.announce_winner()
            print(f"Number of Moves: {game.n_moves}")
            break
        
        game.check_rows_columns_state(move=current_move)
        game.winner = game.is_winner()
        if game.winner:
            game.announce_winner()
            print(f"Number of Moves: {game.n_moves}")
            break

        game.update_valid_moves()
        game.switch_turns()
    
    if not game.winner:
        print("Game ended in Stalemate")

@timeit
@profiler    
def main():
    n_games = 1000
    for _ in range(n_games):
        play_game()

if __name__ == "__main__":
    main()