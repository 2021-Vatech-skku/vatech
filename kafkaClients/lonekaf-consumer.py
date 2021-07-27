from kafka import KafkaConsumer
from json import loads
from time import sleep

# # 카프카 서버
bootstrap_servers = ["localhost:9095"]

# # 카프카 토픽
str_topic_name    = 'lone-p1r1'

# # 카프카 소비자 group1 생성
str_group_name = 'lone-p1r1g1'

# consumer = KafkaConsumer(str_topic_name, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest', enable_auto_commit=True, group_id=str_group_name, value_deserializer=lambda x: loads(x.decode('utf-8')),consumer_timeout_ms=60000 )

# for message in consumer:print(message)


#-------------comsumption data from Faker-----------
# consumer = KafkaConsumer(
#     'test-p6r3',         #kafka topic name
#     bootstrap_servers=["localhost:9092","localhost:9093","localhost:9094"],   #kafka server - local docker-compose kafka
#     #auto_offset_reset='earliest',  #가장 처음 offset부터
#     auto_offset_reset='earliest', # offset 정보가 없으면 예외발생 
#     enable_auto_commit=True,   #마지막으로 읽은 offset 위치 commit
#     auto_commit_interval_ms=500, #offset commit 주기, default : 5000
#     group_id='p6r3g1', #이 consumer가 생성될 consumer group
#     value_deserializer=lambda x: loads(x.decode('utf-8')) #serialize된 메시지를 deserialize
# )
# for event in consumer:
#     event_data = event.value
#     # Do whatever you want
#     print(event_data)
#     #sleep(3)



#----------for performance test----------
consumer = KafkaConsumer(
    bootstrap_servers,
    auto_offset_reset = 'earliest',
    group_id = 'lone-p1r1g1'
)