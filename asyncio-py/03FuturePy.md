## 手动Future用法
```python
from concurrent.futures import Future

# 创建 Future 对象 future
future = Future()

# 给 future 绑定回调
def callback(f: Future):
    print("当set_result的时候会执行回调，result:",
          f.result())
          # f.result(timeout=2))

future.add_done_callback(callback)
future.set_result("嘿嘿")

"""
当set_result的时候会执行回调，result: 嘿嘿
"""
```
注意：只能执行一次 set_result，但是可以多次调用 result 获取结果

## 使用线程池

```python
from concurrent.futures import (
    ThreadPoolExecutor
)
import time

def task(name, n):
    time.sleep(n)
    return f"{name} 睡了 {n} 秒"

executor = ThreadPoolExecutor()
future = executor.submit(task, "古明地觉", 3)


```

## 多线程
```python
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)
import time

def task(name, n):
    time.sleep(n)
    return f"{name} 睡了 {n} 秒"

executor = ThreadPoolExecutor()
futures = [executor.submit(task, "古明地觉", 3),
           executor.submit(task, "古明地觉", 4),
           executor.submit(task, "古明地觉", 1)]

# 使用for拿值（按照提交顺序取值）
for future in futures:
    print(future.result())
# 这里是直接去拿结果，所以没有完成的就会等待，总时间是最长的一个时间


# 按照完成顺序拿值
for future in as_completed(futures):
    print(future.result())
```

## 线程取消
前提，panding状态的线程
```python
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)
import time

def task(name, n):
    time.sleep(n)
    return f"{name} 睡了 {n} 秒"
executor = ThreadPoolExecutor(max_workers=2)
future1 = executor.submit(task, "古明地觉", 1)
future2 = executor.submit(task, "古明地觉", 2)
future3 = executor.submit(task, "古明地觉", 3)
# 如果池子里可以创建空闲线程
# 那么函数一旦提交就会运行，状态为 RUNNING
print(future1._state)  # RUNNING
print(future2._state)  # RUNNING
# 但 future3 内部的函数还没有运行
# 因为池子里无法创建新的空闲线程了，所以状态为 PENDING
print(future3._state)  # PENDING
# 取消函数的执行，前提是函数没有运行
# 会将 future 的 _state 属性设置为 CANCELLED
future3.cancel()
# 查看是否被取消
print(future3.cancelled())  # True
print(future3._state)  # CANCELLED
```

## 线程错误
```python
from concurrent.futures import ThreadPoolExecutor

def task1():
    1 / 0

def task2():
    pass

executor = ThreadPoolExecutor(max_workers=2)
future1 = executor.submit(task1)
future2 = executor.submit(task2)
print(future1.exception())
# ZeroDivisionError: division by zero
print(future2.exception())  
# None
```

## 等待函数执行完毕
```python
from concurrent.futures import (
    ThreadPoolExecutor,
    wait
)
import time

def task(n):
    time.sleep(n)
    return f"sleep {n}"

executor = ThreadPoolExecutor()

future1 = executor.submit(task, 5)
future2 = executor.submit(task, 2)
future3 = executor.submit(task, 4)


for future in [future1, future2, future3]:
    print(future.result())

fs = wait([future1, future2, future3],
          return_when="ALL_COMPLETED")
print(fs.done)
print(fs.not_done)
for f in fs.done:
    print(f.result())

with ThreadPoolExecutor() as executor:
    future1 = executor.submit(task, 5)
    future2 = executor.submit(task, 2)
    future3 = executor.submit(task, 4)


executor.shutdown()
```

## 进程池
```python
from concurrent.futures import ProcessPoolExecutor
import time

def task(n):
    time.sleep(n)
    return f"sleep {n}"

executor = ProcessPoolExecutor()
# Windows 上需要加上这一行
```