from kafka import SimpleProducer, SimpleClient
import time

# To send messages asynchronously
host = '127.0.0.1'
port = 9092
bootstrap_servers = '%s:%s' % (host, port)
client = SimpleClient(bootstrap_servers)
producer = SimpleProducer(client, async=True)
# producer = SimpleProducer(client, async=False)


i = 0
start_time = time.time()
# producer.send_messages('test', b'hello')
try:
    while True:
        i += 1
        body = 'cpy %s' % i
        msg = bytes(body, encoding='utf-8')
        producer.send_messages('test', msg)
        print(body)
        use_time = time.time() - start_time
        if use_time > 1:
            rate = i/use_time
            print('发送速率：%s' % rate)
            # break
        # if i == 100000:
        #     print(i, use_time)
        #     break
except:
    print(i)
