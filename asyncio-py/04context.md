## python context 疑问 (answer from gpt4)
* Python 的协程是无栈协程？
```text
Python的协程（coroutine）是一种特殊的生成器（generator），它们是有栈的，但这个栈与操作系统的线程栈不同，它是在Python解释器级别实现的。Python的协程是基于生成器的，因此它们的栈是由生成器的迭代器堆栈实现的。

Python的协程是一种用户级别的，可以由程序员在代码中明确控制的轻量级线程。它们不需要操作系统的介入就可以进行上下文切换，因此在某些情况下，它们比操作系统级别的线程更高效。

Python的协程可以通过yield关键字进行暂停和恢复，这使得它们可以在一个函数的中间返回一个值，然后在稍后的某个时间点从这个位置继续执行。这种能力使得协程非常适合用于处理并发活动，如IO操作、事件驱动编程等。

Python 3.5及以上版本引入了新的async/await语法来创建和管理协程，这使得协程的使用变得更加简单和直观。

```
* 为什么有栈却不能实现context
```text
Python的协程虽然有栈，但这个栈是在Python解释器级别实现的，它与操作系统的线程栈不同。Python的协程是基于生成器的，因此它们的栈是由生成器的迭代器堆栈实现的。这种栈结构主要用于保存函数调用的状态，而不是用于保存上下文（context）。

在计算机科学中，上下文通常指的是程序执行的环境，包括程序的运行状态、局部变量、全局变量、堆栈、寄存器状态等。在多线程或多进程环境中，当一个线程或进程被切换出CPU时，它的上下文会被保存下来，以便在稍后的某个时间点恢复执行。

然而，Python的协程并不是真正的线程或进程，它们是在Python解释器级别实现的用户级线程。Python的协程不能直接访问或操作操作系统级别的上下文，因此它们不能实现上下文切换。

Python的协程主要用于处理并发活动，如IO操作、事件驱动编程等。它们通过yield关键字进行暂停和恢复，这使得它们可以在一个函数的中间返回一个值，然后在稍后的某个时间点从这个位置继续执行。这种能力使得协程非常适合用于处理并发活动，但并不适合用于实现上下文切换。
```

* python的协程和golang的协程有什么区别
```text
Python的协程和Go语言的协程在设计和实现上有一些重要的区别：

设计理念：Python的协程是基于生成器的，主要用于处理并发活动，如IO操作、事件驱动编程等。Python的协程通过yield关键字进行暂停和恢复，这使得它们可以在一个函数的中间返回一个值，然后在稍后的某个时间点从这个位置继续执行。而Go语言的协程（goroutine）是语言内建的并发构造，它们是轻量级的线程，可以在任何函数或方法上启动。

调度：Python的协程是协作式的，也就是说，它们需要显式地将控制权交给其他协程。如果一个Python协程不显式地放弃控制权，那么其他协程就无法运行。而Go语言的协程是由Go运行时系统进行调度的，它们可以在任何时候被抢占，这使得Go语言的协程更像是真正的线程。

性能：由于Python的全局解释器锁（GIL）的存在，Python的协程在多核CPU上无法实现真正的并行。即使在多线程环境中，Python的解释器在任何时刻都只会执行一个线程。而Go语言的协程可以在多核CPU上实现真正的并行，这使得Go语言在处理并发任务时具有更高的性能。

内存消耗：Python的协程是基于生成器的，因此它们的内存消耗相对较小。而Go语言的协程虽然也是轻量级的，但它们的内存消耗通常会比Python的协程稍大一些。

错误处理：Python的协程可以通过异常进行错误处理，而Go语言的协程需要通过显式的错误检查和恢复机制进行错误处理。

语法：Python 3.5及以上版本引入了新的async/await语法来创建和管理协程，这使得协程的使用变得更加简单和直观。而Go语言的协程通过go关键字启动，通过通道（channel）进行通信，语法更为简洁。
```

* python的协程和golang的协程context区别
```text

Python和Go语言的协程在上下文（context）管理上有一些重要的区别：

Python的协程上下文：Python的协程是基于生成器的，它们的上下文主要由生成器的迭代器堆栈实现。这种栈结构主要用于保存函数调用的状态，而不是用于保存上下文。Python的协程不能直接访问或操作操作系统级别的上下文，因此它们不能实现上下文切换。Python 3.7引入了contextvars模块，该模块提供了一个新的API来管理、存储和访问在逻辑上独立的上下文。

Go语言的协程上下文：Go语言的协程（goroutine）是语言内建的并发构造，它们是轻量级的线程，可以在任何函数或方法上启动。Go语言的协程可以直接访问和操作操作系统级别的上下文，因此它们可以实现上下文切换。Go语言还提供了一个context包，该包定义了Context类型，它是在API边界之间传递截止日期、取消信号和其他请求范围的值的一种方式。

总的来说，Go语言的协程在上下文管理上更为强大和灵活，它们可以直接访问和操作操作系统级别的上下文，可以实现上下文切换，并且提供了一个专门的context包来管理和传递上下文。而Python的协程在上下文管理上相对较弱，它们不能直接访问和操作操作系统级别的上下文，不能实现上下文切换，但Python 3.7及以上版本提供了contextvars模块来管理、存储和访问在逻辑上独立的上下文。
```
## ThreadLocal
它专门用来创建局部变量，并且创建的局部变量是和线程绑定的。
```python
import threading

# 创建一个 local 对象
local = threading.local()

def get():
    name = threading.current_thread().name
    # 获取绑定在 local 上的 value
    value = local.value
    print(f"线程: {name}, value: {value}")

def set_():
    name = threading.current_thread().name
    # 为不同的线程设置不同的值
    if name == "one":
        local.value = "ONE"
    elif name == "two":
        local.value = "TWO"
    # 执行 get 函数
    get()

t1 = threading.Thread(target=set_, name="one")
t2 = threading.Thread(target=set_, name="two")
t1.start()
t2.start()
```

## ContextVar

ContextVar 提供了两个方法，分别是 get 和 set，用于获取值和设置值

一个协程内部 await 另一个协程，另一个协程内部 await 另另一个协程，不管套娃（await）多少次，它们获取的值都是一样的。并且在任意一个协程内部都可以重新设置值，然后获取会得到最后一次设置的值

```python
import asyncio
import contextvars

c = contextvars.ContextVar("只是一个标识, 用于调试")

async def get1():
    return await get2()

async def get2():
    val = c.get() + "~~~"
    c.set("重新设置啦")
    return val

async def set_(val):
    # 设置值
    c.set(val)
    print(await get1())
    print(c.get())

async def main():
    coro = set_("古明地觉")
    await coro

asyncio.run(main())
"""
古明地觉~~~
重新设置啦
"""
```



ContextVar可以设置默认值

```python
import contextvars
c = contextvars.ContextVar("只是一个标识, 用于调试", default="哼哼")

# 或者获取的时候
c.get("古明地恋")
```
当 ContextVar 和 get 中都没有指定默认值，会抛出 LookupError；
只要有一方设置了，那么会得到默认值；
如果都设置了，那么以 get 为准；

## ContextVar和threading.local 的表现是一样的，但是更建议使用 ContextVars。不过前者可以绑定任意多个值，而后者只能绑定一个值（可以通过传递字典的方式解决这一点。

## ContextVar一些用法
当我们调用 c.set 的时候，其实会返回一个 Token 对象：
```python
import contextvars

c = contextvars.ContextVar("context_var")
token = c.set("val")
print(token)
"""
<Token var=<ContextVar name='context_var' at 0x00..> at 0x00...>
"""

# Token 对象有一个 var 属性，它是只读的，会返回指向此 token 的 ContextVar 对象
print(token.var is c)  # True
print(token.var.get())  # val

print(
    token.var.set("val2").var.set("val3").var is c
)  # True
print(c.get())  # val3


# Token 对象还有一个 old_value 属性，它会返回上一次 set 设置的值，如果是第一次 set，那么会返回一个 <Token.MISSING>。
print(token.old_value)  # <Token.MISSING>
token = c.set("val2")
print(c.get())  # val2
# 返回上一次 set 的值
print(token.old_value)  # val

# 和 reset 搭配使用，可以对状态进行重置
c.reset(token)
print(c.get("默认值"))  # 默认值
```

## contextvars.Context

它负责保存 ContextVars 对象和设置的值之间的映射，但是我们不会直接通过 contextvars.Context 来创建，而是通过 contentvars.copy_context 函数来创建。

```python
import contextvars

c1 = contextvars.ContextVar("context_var1")
c1.set("val1")
c2 = contextvars.ContextVar("context_var2")
c2.set("val2")

context = contextvars.copy_context()

def change(val1, val2):
    c1.set(val1)
    c2.set(val2)
    print(c1.get(), context[c1])
    print(c2.get(), context[c2])

# 在 change 函数内部，重新设置值
# 然后里面打印的也是新设置的值
context.run(change, "VAL1", "VAL2")
"""
VAL1 VAL1
VAL2 VAL2
"""

print(c1.get(), context[c1])
print(c2.get(), context[c2])
"""
val1 VAL1
val2 VAL2
"""
```
如果在里面修改了 ContextVar 实例设置的值，那么对于 ContextVar 而言只会在函数内部生效，一旦出了函数，那么还是原来的值。但是对于 Context 而言，它是会受到影响的，即便出了函数，也是新设置的值，因为它直接把内部的字典给修改了