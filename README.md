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


thread = rethread.thread(my_long_function)

with thread as t: # this will run everything in this block while the above thread is running, and then wait for it to finish.
    some_other_function()
    another_function(t)

print(thread.value) # get the return value of the thread
```

## Usage

### Creating a thread

To create a thread, pass a function into the `rethread.thread` function. For example:

```py
import rethread
import time

def long_function():
    time.sleep(10)

thread = rethread.thread(long_function)
```

If you would like to pass additional parameters, just add them after the callable in your `thread` call, like this:

```py
thread = rethread.thread(long_function, 'a', 'b', 'c', some_kwarg = 'abc')
```

### Using a thread

Once you have created your thread, you can do a number of things.

One of the most common use cases will be running the thread, doing something else in the meantime, and then waiting for it to finish. This can be done using the `rethread.RunningThread` context manager, like so:

```py
import rethread
import time

def long_function():
    time.sleep(10)
    return 'hello'

def new_long_function():
    time.sleep(3)

thread = rethread.thread(long_function)

with thread:
    new_long_function()
# waits for the thread to finish
```

You can also wait for the thread to finish without the context manager using the `RunningThread.wait()` function.

```py
thread = rethread.thread(long_function)
thread.wait() # waits for the thread to finish
```

Now, if you don't want to wait for the thread to finish, but just check if it's still running, you can check the `RunningThread.done` property. For example:

```py
import rethread
import time

def long_function():
    time.sleep(10)

thread = rethread.thread(long_function)
print(thread.done) # False
thread.wait()
print(thread.done) # True
```

There's a good chance that you need the return value of the thread you're waiting on. Library's and packages like `threading` don't have a good way of doing this. However, rethread makes this easy with the `RunningThread.value` property:

```py
import rethread
import time

def long_function():
    time.sleep(10)
    return 'hello world'

def some_other_function():
    ...

thread = rethread.thread(long_function)

with thread:
    some_other_function()

print(thread.value) # "hello world"
```

**Warning:** Rethread will raise an error if you try to read the value before the thread is finished. If you want to check if the value is set without waiting, you can use the `done` property or the `value_set` property, like this:

```py
import rethread
import time

def long_function():
    time.sleep(10)
    return 'hello world'

thread = rethread.thread(long_function)

if thread.value_set:
    print(thread.value)
else:
    print('not finished yet!')

# prints "not finished yet!"
```
