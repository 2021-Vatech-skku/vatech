from kafka import KafkaProducer
from json import dumps
import time
from time import sleep
from data import get_registered_user
from data import calculate_thoughput

msg_count = 500000
msg_size = 100 #100 bytes
msg_payload = ('testmessage'*20).encode()[:msg_size]

def on_send_success(record_metadata):
    print("topic recorded:",record_metadata.topic)
    print("partition recorded:",record_metadata.partition)
    print("offset recorded:",record_metadata.offset)

def on_send_error(excp):
        print(excp)
    
# 카프카 서버
bootstrap_servers = ["localhost:9095"]

# 카프카 공급자 생성
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         key_serializer=None,
                         acks=0,
                         #linger_ms=500,
                         #value_serializer=lambda x: dumps(x).encode('utf-8')
                        )

# 카프카 토픽
str_topic_name = 'lone-p1r1'



#---------performance test-----------------
producer_start = time.time()

for i in range(msg_count):
    producer.send(str_topic_name,
                  msg_payload
    )#.add_callback(on_send_success).add_errback(on_send_error)

producer.flush()
time_elapsed = time.time() - producer_start


calculate_thoughput(time_elapsed,msg_count,msg_size)
#time.sleep(300000)
