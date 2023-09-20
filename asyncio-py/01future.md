## 基本future
```python
from asyncio import Future

future1 = Future()

future1.set_result("HELLO")
# future1.set_exception(ValueError("kkk"))

print(future1.done())
print(future1.result())
print(future1.exception())
```
Future 是 Python 的一个类,它包含一个你希望在未来某个时间点获得、但目前还不存在的值。通常，当创建 future 时，它没有任何值，因为还不存在。

可以简单理解为我们发出了一个请求，由于请求需要一些时间，所以 future 还处于 pending 状态。当请求完成时，结果将被设置，那么 future 会变成 finished 状态，我们就可以访问它了

注意：我们只能调用一次 set_result，但是 result 可以多次调用。

## 源码future
首先 Future 实例有三个非常重要的属性：_state、_result、_exception，含义如下。

_state 表示运行状态，总共三种，分别是：PENDING（正在运行）、CANCELLED（已取消）、FINISHED（已完成）
_result：调用 future.set_result() 时，本质上就是将结果值设置给了该属性
_exception：调用 future.set_exception() 时，本质上就是将异常设置给了该属性

```python
class Future:
    
    def cancel(self):
        # cancel 方法，负责取消一个 future
        # 并且该方法有返回值，取消成功返回 True，取消失败返回 False
        self.__log_traceback = False
        # 检测状态是否为 PENDING，不是 PENDING，说明 future 已经运行完毕或取消了
        # 那么返回 False 表示取消失败，但对于 future 而言则无影响
        if self._state != _PENDING:
            return False
        # 如果状态是 PENDING，那么将其改为 CANCELLED
        self._state = _CANCELLED
        self.__schedule_callbacks()
        return True

    def cancelled(self):
        # 判断 future 是否被取消，那么检测它的状态是否为 CANCELLED 即可
        return self._state == _CANCELLED

    def done(self):
        # 判断 future 是否已经完成，那么检测它的状态是否不是 PENDING 即可
        # 注意：CANCELLED 和 FINISHED 都表示 future 运行结束
        return self._state != _PENDING

    def result(self):
        # 调用 result 方法相当于获取 future 设置的结果
        # 但如果它的状态为 CANCELLED，表示取消了，那么抛出 CancelledError
        if self._state == _CANCELLED:
            raise exceptions.CancelledError
        # 如果状态不是 FINISHED（说明还没有设置结果）
        # 那么抛出 asyncio.InvalidStateError 异常
        # 所以我们不能在 set_result 之前调用 result
        if self._state != _FINISHED:
            raise exceptions.InvalidStateError('Result is not ready.')
        self.__log_traceback = False
        # 走到这里说明状态为 FINISHED
        # 但不管是正常执行、还是出现异常，都会将状态标记为 FINISHED
        # 如果是出现异常，那么调用 result 会将异常抛出来
        if self._exception is not None:
            raise self._exception
        # 否则返回设置的结果
        return self._result

    def exception(self):
        # 无论是 set_result，还是 set_exception，future 的状态都是已完成
        # 如果是前者，那么 self._result 就是结果，self._exception 为 None
        # 如果是后者，那么 self._result 为 None，self._exception 就是异常本身
        
        # 因此调用 result 和 exception 都要求 future 的状态为 FINISHED
        # 如果为 CANCELLED，那么同样抛出 CancelledError
        if self._state == _CANCELLED:
            raise exceptions.CancelledError
        # 如果为 PENDING，那么抛出 asyncio.InvalidStateError 异常
        if self._state != _FINISHED:
            raise exceptions.InvalidStateError('Exception is not set.')
        self.__log_traceback = False
        # 返回异常本身
        # 因此如果你不确定 future 内部到底是普通的结果值，还是异常
        # 那么可以先调用 future.exception()，看它是否为 None
        # 如果 future.exception() 不为 None，那么拿到的就是异常
        return self._exception

    def set_result(self, result):
        # 通过 set_result 设置结果
        # 显然在设置结果的时候，future 的状态应该为 PENDING 
        if self._state != _PENDING:
            raise exceptions.InvalidStateError(f'{self._state}: {self!r}')
        # 然后设置 self._result，当程序调用 future.result() 时会返回 self._result
        self._result = result
        # 并将状态标记为 FINISHED，表示一个任务从 PENDING 变成了 FINISHED
        # 所以我们不能对一个已完成的 future 再次调用 set_result
        # 因为第二次调用 set_result 的时候，状态已经不是 PENDING 了
        self._state = _FINISHED
        self.__schedule_callbacks()

    def set_exception(self, exception):
        # 和 set_result 类似，都表示任务从 PENDING 变成 FINISHED
        if self._state != _PENDING:
            raise exceptions.InvalidStateError(f'{self._state}: {self!r}')
        # 但 exception 必须是异常，且不能是 StopIteration 异常
        if isinstance(exception, type):
            exception = exception()
        if type(exception) is StopIteration:
            raise TypeError("StopIteration interacts badly with generators "
                            "and cannot be raised into a Future")
        # 将 self._exception 设置为 exception
        # 调用 future.exception() 的时候，会返回 self._exception
        self._exception = exception
        # 将状态标记为已完成
        self._state = _FINISHED
        self.__schedule_callbacks()
        self.__log_traceback = True
```

