import time
import functools

def calculate_execution_time(func):
    @functools.wraps(func)  # Preserves the original function's metadata
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # More accurate timer
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        else:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.6f} seconds")  # Precision to microseconds
            return result
    return wrapper