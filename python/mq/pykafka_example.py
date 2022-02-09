# -* coding:utf8 *-
from pykafka import KafkaClient
import time

hosts = '1127.0.0.1:9092'
client = KafkaClient(hosts=hosts)
# client = KafkaClient(hosts="%s:32769" % host)

print(client.topics)

# # 生产者
# topicdocu = client.topics[b'task_pull']
# producer = topicdocu.get_producer()
# for i in range(4):
#     print(i)
#     producer.produce(bytes('test message %s' % (str(i ** 2), ), encoding="utf8"))
# producer.stop()

# 消费者
topic = client.topics[b'test']
consumer = topic.get_simple_consumer(consumer_group=b'test1',
                                     auto_commit_enable=True,
                                     auto_commit_interval_ms=1,
                                     consumer_id=b'test')
i = 0
start_time = time.time()
for message in consumer:
    if message is not None:
        i += 1
        use_time = time.time() - start_time
        if use_time > 1:
            rate = i / use_time
            print('接收速率：%s' % rate)
        print(message.offset, message.value)
            # break
        # if i == 100000:
        #     print(i, use_time)
        #     break
