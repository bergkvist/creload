import multiprocessing as mp
from functools import wraps


def subprocess(fn):
    """Decorate a function to hint that it should be run in a forked subprocess"""
    @wraps(fn)
    def wrapped_fn(*args, **kwargs):
        return subprocess_call(fn, *args, **kwargs)
    return wrapped_fn


def subprocess_call(fn, *args, **kwargs):
    """Executes a function in a forked subprocess"""
    
    ctx = mp.get_context('fork')
    q = ctx.Queue(1)
    is_error = ctx.Value('b', False)
    
    def target():
        try:
            q.put(fn(*args, **kwargs))
        except BaseException as e:
            is_error.value = True
            q.put(e)
    
    ctx.Process(target=target).start()
    result = q.get()    
    if is_error.value:
        raise result
    
    return result
