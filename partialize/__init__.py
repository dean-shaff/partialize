import functools
import inspect
import logging

__all__ = [
    "partialize"
]

__version__ = "0.2.0"

module_logger = logging.getLogger(__name__)


def _get_required_args(func):
    """
    Determine the number of required arguments for a given function.
    """
    module_logger.debug(f"_get_required_args: func={func}")
    fas = inspect.getfullargspec(func)
    module_logger.debug(f"_get_required_args: fas={fas}")
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
        module_logger.debug(f"_partialize: args={args}, kwargs={kwargs}")
        sig = inspect.signature(func)
        ba = sig.bind_partial(*args, **kwargs)
        ba.apply_defaults()
        ba_args, ba_kwargs = ba.args, ba.kwargs
        if "args" in ba_kwargs and "args" not in kwargs:
            del ba_kwargs["args"]
        module_logger.debug(
            f"_partialize: ba_args={ba_args}, ba_kwargs={ba_kwargs}")
        partial = functools.partial(func, *ba_args, **ba_kwargs)
        required_args = _get_required_args(partial)
        if required_args == 0:
            return partial()
        else:
            return partialize(partial)

    return _partialize
