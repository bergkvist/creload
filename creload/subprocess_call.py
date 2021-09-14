import multiprocessing as mp


class subprocess:
    """Decorate a function to hint that it should be run in a forked subprocess"""
    def __init__(self, fn):
        self.fn = fn
    def __call__(self, *args, **kwargs):
        return subprocess_call(self.fn, *args, **kwargs)


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
