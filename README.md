# ReThread

## Minimalistic Python Library for Easy Multithreading

### Installation

#### Linux/Mac

```
python3 -m pip install -U rethread
```

#### Windows

```
py -3 -m pip install -U rethread
```

### Example

```py
import rethread
import time

@rethread.auto
def my_long_function():
    time.sleep(10)

    return 'a'

def some_other_function():
    for i in range(3):
        time.sleep(1)
        print(i)

def another_function(t: rethread.RunningThread):
    time.sleep(10)

    if t.done:
        print('thread is finished!')


with my_long_function() as t:
    some_other_function()
    another_function(t)

print(thread.value)
```

## Usage

To create a thread, you can use the `rethread.thread` function, like so:

```py
import rethread

def long_function():
    ...

thread: rethread.RunningThread = rethread.thread(long_function)
```

If you would like to pass in parameters, simply pass them in to the `*args` and `**kwargs` of the `rethread.thread` call. For example:

```py
import rethread

def long_function(a: str, b: str, some_kwarg: str = 'c'):
    ...

thread: rethread.RunningThread = rethread.thread(long_function, 'a', 'b', some_kwarg = 'c')
```

If you plan on always running a function in a thread, you can use `rethread.auto` to automatically thread a function:

```py
@rethread.auto
def long_function():
    ...

thread: rethread.RunningThread = long_function() # no need for a call to rethread.thread
```

To get the return value of the threaded function, access the `RunningThread.value` attribute.

An error will be raised if the thread is still running, so make sure to call `wait()` on the thread.

```py
@rethread.auto
def long_function() -> str:
    ...

    return 'hi'

t = long_function()
t.wait() # wait for the thread to finish
print(t.value) # hi
```

Alternatively, you can use the context manager syntax to automatically wait for the thread to finish:

```py
@rethread.auto
def long_function() -> str:
    ...

    return 'hi'

t = long_function()
with t:
    do_something()
    # once everything in this context is finished, rethread automatically waits for the thread to finish

print(t.value) # hi
```
