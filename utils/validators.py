import functools

def strict_move_validation_check(func):
    """Decorator to perform additional validation on ConnectTetra class move execution if strict_mode is enabled"""
    @functools.wraps(func)
    def wrapper(connect_tetra, player, move: int):
        if connect_tetra.strict_mode:
            if player != connect_tetra.current_player:
                raise ValueError(f"It is not {player.name}'s turn. Current player is {connect_tetra.current_player.name}.")
        return func(connect_tetra, player, move)
    return wrapper