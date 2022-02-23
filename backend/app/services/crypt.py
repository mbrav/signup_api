import cProfile
import functools
import inspect
import time

from passlib import hash


def timer(func):
    """Timer Decorator for measuring execution performance

    Args:
        none

    Returns:
        value
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()

        value = func(*args, **kwargs)

        run_time = time.perf_counter() - start_time

        print(f"finished in {run_time:.4f} secs")
        # print(f"Finished {func.__name__!r} in {run_time:.4f} secs")

        return value
    return wrapper_timer


@timer
def run_hash(func, salt: int = 8, password: str = 'password'):

    txt = '{:<25} {:<5} \t'.format(func.__name__, salt)
    print(txt, end=" ")
    try:
        func.using(salt_size=16).hash(password)
        func.hash(password)
    except Exception as e:
        pass


if __name__ == '__main__':
    print('{:<25} {:<5} \t'.format('name', 'salt'))
    for name, obj in inspect.getmembers(hash):
        if name.startswith('__'):
            continue
        if inspect.isclass(obj):
            run_hash(obj)

    # run_hash(hash.pbkdf2_sha256)
    # run_hash(hash.md5_crypt)
