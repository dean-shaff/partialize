import functools
import inspect

__all__ = [
    "partialize"
]

__version__ = "0.1.0"


def _get_required_args(func):
    """
    Determine the number of required arguments for a given function.
    """
    fas = inspect.getfullargspec(func)
    len_args = len(fas.args)
    len_args += len(fas.kwonlyargs)
    if fas.kwonlydefaults is not None:
        len_args -= len(fas.kwonlydefaults)
    if fas.defaults is not None:
        len_args -= len(fas.defaults)
    return len_args


def partialize(func):

    @functools.wraps(func)
    def _partialize(*args, **kwargs):
        sig = inspect.signature(func)
        ba = sig.bind_partial(*args, **kwargs)
        ba.apply_defaults()
        partial = functools.partial(func, *ba.args, **ba.kwargs)
        required_args = _get_required_args(partial)
        if required_args == 0:
            return partial()
        else:
            return partialize(partial)

    return _partialize
