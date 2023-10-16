from concurrent.futures import Future

future = Future()
future.set_result("哼哼")

print(future.result(timeout=2))  # 哼哼