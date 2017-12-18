#!/usr/bin/env python
# -*-coding:utf-8 -*-

import pika
import time

host = '127.0.0.1'
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.3'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

start_time = time.time()

i = 0


def callback(ch, method, properties, body):
    # time.sleep(5)
    global i
    i += 1
    use_time = time.time() - start_time
    print(body)
    if use_time > 1:
        rate = i / use_time
        print('消费速率：%s' % rate)
    # print(" [x] Received : %r" % body)
    # time.sleep(body.count(b'.'))
    # print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=10000)
# channel.basic_qos(prefetch_count=60000)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
