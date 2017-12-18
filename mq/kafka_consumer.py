from kafka import KafkaConsumer
import time

host = '127.0.0.1'
port = 9092
bootstrap_servers = '%s:%s' % (host, port)
consumer = KafkaConsumer('test', bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest')

i = 0
start_time = time.time()
try:
    for m in consumer:
        # print(m)
        i += 1
        use_time = time.time() - start_time
        if use_time > 1:
            rate = i/use_time
            print('接收速率：%s' % rate)
        # if i == 1000000:
        #     print(i, use_time)
        #     break
except:
    print(i, use_time)

