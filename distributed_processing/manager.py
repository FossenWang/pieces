"""
https://docs.python.org/3/library/multiprocessing.html#managers
"""

from multiprocessing import Process
from multiprocessing.managers import BaseManager

from time import sleep


def run_task(info):
    print('task processing')
    sleep(3)
    print('received info: ' + str(info))
    print('task finished')


def receive_task(info=None):
    p = Process(target=run_task, args=(info,))
    p.start()
    return 0


BaseManager.register('send_task', callable=receive_task)

# 绑定端口5000, 设置验证码'abc':
manager = BaseManager(address=('', 5000), authkey=b'abc')

if __name__ == '__main__':
    server = manager.get_server()
    print('server start')
    server.serve_forever()
