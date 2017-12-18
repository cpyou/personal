#-*- coding:utf-8 -*-

import time
import sys
import stomp
from random import randint

start_time = time.time()

i = 0


class MyListener(stomp.ConnectionListener):

    def __init__(self, conn):
        self.cnt = 0
        self.conn = conn

    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        global i
        i += 1
        self.cnt += 1
        # print('调用activemq header: %s; message: %s; cpy %s' % (headers, message, self.cnt))
        use_time = time.time() - start_time
        print(message)
        if use_time > 1:
            rate = i / use_time
            print('生产速率：%s' % rate)
        print('message: %s; cpy %s' % (message, self.cnt))
        # sec = randint(0,3)
        # time.sleep(sec)
        #exit()
        self.conn.ack(headers['message-id'])
        #exit()


host = '127.0.0.1'
conn = stomp.Connection10([(host, 61613)])
conn.set_listener('', MyListener(conn))
conn.start()
conn.connect('admin', 'admin')
conn.subscribe(destination='cpytestQueue', ack='client')
# conn.subscribe(destination='cpytestQueue', id=1)

i = 0
while True:
    try:
        time.sleep(60)
        # i += 1
        # print '订阅：%s' % i
       # conn.subscribe(destination='cpytestQueue')
    except:
        break


time.sleep(2)
conn.disconnect()
