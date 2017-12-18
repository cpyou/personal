#!/usr/bin/env python
# -*-coding:utf-8 -*-
import pika
import sys
import time

# host = '192.168.181.129'
host = '127.0.0.1'
# host = '192.168.181.128'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


# for i in range(10):
#     message = ' '.join(sys.argv[1:]) or "Hello World %s!" % i
#     channel.basic_publish(exchange='',
#                           routing_key='task_queue',
#                           body=message,
#                           properties=pika.BasicProperties(
#                               delivery_mode=2,  # make message persistent
#                           ))
#     print(" [x] Sent %r" % message)
# connection.close()

try:
    i = 0
    start_time = time.time()
    while 1:
        i += 1
        message = "cpy %s" % i
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        use_time = time.time() - start_time
        print(message)
        if use_time > 1:
            rate = i / use_time
            print('生产速率：%s' % rate)
            # break
        # print(" [x] Sent %r" % message)
        # num = 6300
        # if i % num == 0:
        #     time.sleep(1)
        #     use_time = num / (time.time() - start_time)
        #     print('速率：%s' % use_time)
        #     start_time = time.time()
        #     print('\n')
except:
    connection.close()
