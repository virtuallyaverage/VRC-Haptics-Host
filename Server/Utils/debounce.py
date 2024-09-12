import time

# https://gist.github.com/walkermatt/2871026

def debounce(s):
    """Decorator ensures function that can only be called once every `s` seconds.
    """
    def decorate(f):
        t = None

        def wrapped(*args, **kwargs):
            nonlocal t
            t_ = time.time()
            if t is None or t_ - t >= s:
                result = f(*args, **kwargs)
                t = time.time()
                return result
        return wrapped
    return decorate

def debounce_class(s_callable):
    """Decorator ensures function can only be called once every `s` seconds."""
    def decorate(f):
        t = None

        def wrapped(self, *args, **kwargs):
            nonlocal t
            s = s_callable(self)  # Evaluate the callable to get the debounce time
            t_ = time.time()
            if t is None or t_ - t >= s:
                result = f(self, *args, **kwargs)
                t = time.time()
                return result
        return wrapped
    return decorate