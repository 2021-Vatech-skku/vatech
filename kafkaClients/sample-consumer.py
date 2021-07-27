from kafka import KafkaConsumer
from json import loads
from time import sleep
import time
from data import calculate_thoughput

# 카프카 서버
bootstrap_servers = ["localhost:9095"]

# 카프카 토픽
str_topic_name    = 'lone-p1r1'

# 카프카 소비자 group 생성
str_group_name = 'g1'

#-------------comsumption data from Faker-----------
consumer = KafkaConsumer(str_topic_name,         #kafka topic name
                         bootstrap_servers= ["localhost:9095"],   #kafka server - local docker-compose kafka
                         auto_offset_reset='earliest',  #가장 처음 offset부터
                         enable_auto_commit=True,   #마지막으로 읽은 offset 위치 commit
                         auto_commit_interval_ms=500, #offset commit 주기, default : 5000
                         #group_id=str_group_name, #이 consumer가 생성될 consumer group
                         value_deserializer=lambda x: loads(x.decode('utf-8')) #serialize된 메시지를 deserialize
                        )
for event in consumer:
     event_data = event.value
     print(event_data)
     sleep(1)

