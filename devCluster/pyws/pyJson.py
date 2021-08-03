# -*- coding: utf-8 -*- 

import json
from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import loads
from time import sleep
import time


def on_send_success(record_metadata):
    print("topic recorded:",record_metadata.topic)
    print("partition recorded:",record_metadata.partition)
    print("offset recorded:",record_metadata.offset)

def on_send_error(excp):
        print(excp)



str_topic_name    = 'jee.clever.dev0-patient.test'
str_group_name = 'g9'

#-------------comsumption data from Faker-----------
consumer = KafkaConsumer(str_topic_name,         #kafka topic name
                         bootstrap_servers= ["kafka-kafka-bootstrap:9093"],   #kafka server - local docker-compose kafka
                         auto_offset_reset='earliest',  
                         enable_auto_commit=True,   
                         auto_commit_interval_ms=500, #offset commit interval, default : 5000
                         #group_id=str_group_name, #
                         connections_max_idle_ms=1000*60*60*26,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')), #
                         key_deserializer=lambda x: json.loads(x.decode('utf-8')),
                         security_protocol= 'SASL_PLAINTEXT',
                         sasl_mechanism='SCRAM-SHA-512',
                         sasl_plain_username='jee-user',
                         sasl_plain_password='kEbUG3h8HWRB'

                        )

producer = KafkaProducer(
                         bootstrap_servers=["kafka-kafka-bootstrap:9093"],
                         key_serializer= lambda x: json.dumps(x).encode('utf-8'),
                         acks=1,
                         connections_max_idle_ms=1000*60*60*25,
                         value_serializer= lambda x: json.dumps(x).encode('utf-8'),
                         security_protocol= 'SASL_PLAINTEXT',
                         sasl_mechanism='SCRAM-SHA-512',
                         sasl_plain_username='jee-user',
                         sasl_plain_password='kEbUG3h8HWRB'
                        )



for message in consumer:
     print("topic=%s\n partition=%d\n offset=%d: \nkey=%s \nvalue=%s" %
        (message.topic,
          message.partition,
          message.offset,
          message.key,
          message.value))

     tempData1 = message.value
     oldFullDocument = tempData1["payload"]["fullDocument"]   #tempData1["payload"]["fullDocument"] == json string
     newStr = json.loads(oldFullDocument)     #json string --> dict
     newStr["name"] = "*****"                 # replace value of dict whose key is "name"
     tempData1["payload"]["fullDocument"] = json.dumps(newStr)  # fullDocument dict --> json string                           
     result = tempData1
     print(result)
     producer.send("jee.clever.dev0-patient.filtered.test",result,message.key)
