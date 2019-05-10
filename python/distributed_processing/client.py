from multiprocessing.managers import BaseManager


manager = BaseManager(address=('127.0.0.1', 5000), authkey=b'abc')
manager.register('send_task')
manager.connect()

print(manager.send_task(1))
print(manager.send_task(2))
print(manager.send_task(3))
