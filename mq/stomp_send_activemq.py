# -*-coding:utf-8 -*-
import time
import sys
import stomp


host = '127.0.0.1'
conn = stomp.Connection12([(host, 61613)])
# conn = stomp.Connection10([(host, 61616)], timeout=10)
conn.start()
conn.connect('admin', 'admin')

# conn.send(body=b'hahah cpy', destination='cpytestQueue', )
i = 0
start_time = time.time()
while True:
    i += 1
    body = 'cpy %s' % i
    conn.send(body=body, destination='cpytestQueue', headers={'persistent': True})
    use_time = time.time() - start_time
    if use_time > 1:
        rate = i/use_time
        print('发送速率：%s' % rate)


time.sleep(2)
conn.disconnect()
