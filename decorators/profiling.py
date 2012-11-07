import cProfile
import time


def cprofile(fun):
    """Wraps function with a cProfile context, which writes profiling
    information to the current working directory.

    Output file is prefixed with the function name and timestamp.
    """
    def wrap(*args, **kwargs):
        command = """fun(*args, **kwargs)"""
        local = locals()
        local['fun'] = fun
        filename = fun.__name__ + '-' + str(time.time()) + ".profile"
        cProfile.runctx(command, globals(), local, filename=filename)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap

