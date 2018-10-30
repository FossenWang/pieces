"""
https://docs.python.org/3/library/multiprocessing.html#managers
"""

from multiprocessing.managers import BaseManager

def print_text(text):
    print(text)

# 绑定端口5000, 设置验证码'abc':
manager = BaseManager(address=('', 5000), authkey=b'abc')

manager.register('print_text', callable=print_text)

server = manager.get_server()
print('server start')
server.serve_forever()
