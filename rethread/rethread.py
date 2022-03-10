from threading import Thread
from typing import Callable, TypeVar, Generic
from typing_extensions import ParamSpec
from functools import wraps

__all__ = (
    "RunningThread",
    "thread",
    "auto"
)

T = TypeVar("T")
P = ParamSpec("P")

class RunningThread(Generic[P, T]):
    """Class representing a running thread."""
    def __init__(self, func: Callable[P, T], *args, **kwargs) -> None:
        self._thread = Thread(target = handler, args = [self, func, args, kwargs])
        self._func = func
        self._value = None
        self._value_set = False
        self._done = False
        self._thread.start()
    
    @property
    def thread(self) -> Thread:
        """Thread object of the running thread."""
        return self._thread
    
    @property
    def func(self) -> Callable[P, T]:
        """Function the thread is running."""
        return self._func
    
    @property
    def value(self) -> T:
        """Return value of the thread."""
        if not self._value:
            raise RuntimeError("thread is not finished, perhaps you forgot to call wait()?")

        return self._value
    
    @value.setter
    def value(self, value: T) -> None:
        if self.value_set:
            raise RuntimeError("value for thread is already set.")
        else:
            self._value_set = True

        self._value = value
    
    @property
    def value_set(self) -> bool:
        """Whether the value has been set."""
        return self._value_set
    
    @property
    def done(self) -> bool:
        """Whether the thread is done."""
        return self._done
    
    @done.setter
    def done(self, value: bool) -> None:
        self._done = value

    def wait(self):
        """Function to wait for the thread to finish."""
        while not self.done:
            pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, *_, **__):
        self.wait()

def handler(instance: RunningThread[P, T], func: Callable[P, T], args: tuple, kwargs: dict):
    resp: T = func(*args, **kwargs)
    
    instance.done = True
    instance.value = resp

def thread(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> RunningThread[P, T]:
    """Function for generating a new running thread."""
    return RunningThread(func, *args, **kwargs)

def auto(func: Callable[P, T]) -> Callable[P, RunningThread[P, T]]:
    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> RunningThread[P, T]:
        return thread(func, *args, **kwargs)
    return inner