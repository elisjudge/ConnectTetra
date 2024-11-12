import cProfile
import pstats
from io import StringIO
import time
import functools

def timeit(func):
    """Decorator to measure the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Starting '{func.__name__}'...")

        result = func(*args, **kwargs)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"'{func.__name__}' completed in {elapsed_time:.2f} seconds.")

        return result
    return wrapper

def profiler(func):
    """Decorator function to profile the performance of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()

        result = func(*args, **kwargs)

        profile.disable()

        stream = StringIO()
        ps = pstats.Stats(profile, stream=stream).sort_stats('cumulative')
        ps.print_stats(20)  # Show top 20 entries
        print(stream.getvalue())

        return result
    return wrapper