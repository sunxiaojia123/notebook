## 判断函数类型
* 如果 co_flags & 0x80 如果为真，那么就是协程函数
* 如果 co_flags & 0x20 如果为真，那么就是生成器函数
* 0x01：优化选项已打开。
* 0x02：新的本地作用域的介绍。
* 0x04：生成器函数。
* 0x08：生成器或协程已经启动，但尚未完成。
* 0x10：*args参数存在。
* 0x20：**kwargs参数存在。
* 0x40：生成器函数。
* 0x80：协程函数。
* 0x100：异步生成器函数。
* 0x200：在函数定义中存在__future__.annotations。

```python
async def coro():
    return "Some Value"
print(coro.__code__.co_flags)
if coro.__code__.co_flags & 0x80:
    print("协程函数")
else:
    print("非协程函数")
```

## 并发比较
```python
import asyncio
import time

async def get_html(n):
    await asyncio.sleep(n)
    print(f"get_html({n})")
    return f"{n} 秒后，页面被下载"

async def main():
    task1 = asyncio.create_task(get_html(3))
    task2 = asyncio.create_task(get_html(2))
    result1 = await task1
    result2 = await task2
    print(result1)
    print(result2)

start = time.perf_counter()
asyncio.run(main())
print("总耗时:", time.perf_counter() - start)
# 总耗时: 3.0027106250054203

print("**20")
async def main2():
    # 得到两个协程对象
    c1 = get_html(3)
    c2 = get_html(2)
    # 协程如果想运行，需要扔到事件循环中进行调度
    # 而包装成任务的时候，会被扔到事件循环中
    # 或者在协程内部通过 await 进行驱动
    result1 = await c1
    result2 = await c2
    print(result1)
    print(result2)

start = time.perf_counter()
asyncio.run(main2())
print("总耗时:", time.perf_counter() - start)
# 总耗时: 5.0034878750448115
```
因此我们不要直接 await 一个协程，而是将它包装成任务

## asyncio用法
```python
import asyncio

async def get_html(n):
    await asyncio.sleep(n)
    print(f"get_html({n})")
    return f"{n} 秒后，页面被下载"

async def main():
    # 创建任务
    long_task = asyncio.create_task(get_html(10))
    # 等待任务
    result1 = await long_task
    # 取消任务
    long_task.cancel()
    try:
        # 引发 CancelledError
        await long_task
    except asyncio.CancelledError:
        print("任务被取消")
    # 设置超时时间
    # 使用 wait_for 必须要搭配 await，阻塞等待任务完成并拿到返回值、或者达到超时时间引发 TimeoutError 之后，程序才能往下执行。
    try:
        result = await asyncio.wait_for(long_task, 1)
    except asyncio.TimeoutError:
        print("超时啦")

    # 超时但是不取消
    try:
        # 通过 asyncio.shield 将 task 保护起来
        result = await asyncio.wait_for(asyncio.shield(long_task), 1)
        print("返回值:", result)
    except asyncio.TimeoutError:
        print("超时啦")
        # 如果超时依旧会引发 TimeoutError，但和之前不同的是
        # 此时任务不会被取消了，因为 asyncio.shield 会将取消请求忽略掉
        print("任务是否被取消:", long_task.cancelled())
        # 从出现超时的地方，继续执行，并等待它完成
        result = await long_task
        print("返回值:", result)
```

## awaitable
Task 是 Future 的子类，而一个任务可以看做是一个 future 和一个协程的组合

协程、future 和任务，都可以使用 await 表达式,它们之间的共同点是 awaitable 抽象基类，这个类定义了一个抽象的魔法函数__await__ ，任何实现了__await__ 方法的对象都可以在 await 表达式中使用
```python
import asyncio
class Girl:

    def __init__(self):
        self.name = "kk"
        self.address = "ll"

    async def get_info(self):
        await asyncio.sleep(1)
        return f"name: {self.name}, address: {self.address}"

    def __await__(self):
        return asyncio.create_task(self.get_info()).__iter__()
    
async def main():
    g = Girl()
    return await g

result = asyncio.run(main())
print(result)
```

## 协程陷阱

* asyncio 使用的是单线程并发模型，这意味着仍然受到单线程和全局解释器锁的限制。
* 第一个场景：代码是 CPU 密集；
* 第二个场景：代码虽然是 IO 密集，但 IO 是同步阻塞 IO，而不是异步非阻塞 IO；
* 同步阻塞 IO，比如 requests.get()、time.sleep() 等，这会阻塞整个线程，导致所有任务都得不到执行；异步非阻塞 IO，比如协程的 IO 操作，这只会阻塞协程，但线程不阻塞，线程可以执行其它已经准备就绪的任务。
* requests 换成 aiohttp 或 httpx



