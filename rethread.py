from threading import Thread, currentThread
from typing import Callable, Any
import inspect
from types import FrameType

class RunningThread:
    def __init__(self, func: Callable, *args, **kwargs) -> None:
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
    def func(self) -> Callable:
        """Function the thread is running."""
        return self._func
    
    @property
    def value(self) -> Any:
        """Return value of the thread."""
        if not self.value_set:
            raise RuntimeError("thread is not finished, perhaps you forgot to call RunningThread.wait()?")
        return self._value
    
    @value.setter
    def value(self, value: Any) -> None:
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
    
    def __exit__(self, *args, **kwargs):
        self.wait()

def handler(instance: RunningThread, func: Callable, args: tuple, kwargs: dict):
    resp: Any = func(*args, **kwargs)
    
    instance.done = True
    instance.value = resp

def thread(func: Callable, *args, **kwargs) -> RunningThread:
    """Function for generating a new running thread."""
    return RunningThread(func, *args, **kwargs)
