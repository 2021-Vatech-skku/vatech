from kafka import KafkaProducer
from json import dumps
import time
from time import sleep
from dev_data import get_registered_user
from dev_data import calculate_thoughput
import sys
import random
import collections
from faker import Faker


def on_send_success(record_metadata):
    print("topic recorded:",record_metadata.topic)
    print("partition recorded:",record_metadata.partition)
    print("offset recorded:",record_metadata.offset)

def on_send_error(excp):
        print(excp)


class fakeDataGenerator:
    def __init__(self):
        self.tmp=[]
    fake = Faker()

    list_sex=["male", "female"]
    list_hospital=[
        ("Vatech","75-11 Seokwoo-dong, Hwaseong-si, Gyeonggi-do","031-379-9500"),
        ("Samsung","81 Ilwon-ro, Ilwon-dong, Gangnam-gu, Seoul","1599-3114"),
        ("Asan","88 Olympic-ro 43-gil, Pungnap 2-dong, Songpa-gu, Seoul","1688-7575")
    ]
    list_patient=[]
    # for i in range(20000):
    #     list_patient.append((fake.uuid4(),fake.name(),fake.address(),fake.pyint(10,80),fake.word(list_sex)))
    
    list_doctor=[]
    for i in range(500):
        list_doctor.append(fake.uuid4())
    
    list_treatment=[ # list from fetch code
        ("Abutment Tightening & Impression",0),("Amalgam Filling",1600000),
        ("Anterior Teeth Resin",7000000),("Basic Care",0),
        ("Bite Wing X-Ray",100000),("CBCT",250000),("Canal Enlargement/Shaping",2000000),
        ("Canal Filling",6000000),("Canal Irrigation",1000000),
        ("Cervical Resin",400000),("Deciduous Tooth Extraction",400000),
        ("Dental Pulp Expiration",500000),("Dressing",0),("GI Filling",300000),
        ("Kontact (France) Implant",175000000),("Metal Braces",45000000),
        ("Neo Biotech SL Implant",60000000),("Oral Exam",0),
        ("Oral Prophylaxis",0),("Orthodontics Diagnosis",0),("PFM-Ni",6000000),("Panorama",400000),
        ("Periapical X-Ray",100000),("Periodonatal Curettage",200000),
        ("Periodontal Probing Depths",0),("Permanent Tooth Extraction",1000000),
        ("Posterial Teeth Resin",500000),
        ("Prosthesis Re-attachment",200000),("Pulpectomy",6000000),("Re-Endo",12000000),
        ("Root Planing",500000),("Scailing",500000),("Simple Bone Graft",4000000),
        ("Temporary Crown",0),("Wisdom Tooth Extraction",6000000),("Working Length",0)
    ]

    list_payment=["cash","card"]

    def gendata(self):
        
        for i in range(100):
            # hospital=random.choice(self.list_hospital)
            # if hospital[1]=="Vatech":
            #     doctor=random.choice(self.list_doctor[:200]) # 200 dentists in Vatech
            # elif hospital[1]=="Samsung":
            #     doctor=random.choice(self.list_doctor[200:350]) # 150 dentists in Samsung
            # else:
            #     doctor=random.choice(self.list_doctor[350:]) # 150 dentists in other dental clinic
            # patient=random.choice(self.list_patient)
            treatment=random.choice(self.list_treatment)
            date=str(self.fake.date_between(start_date="-2y"))      #date_between(start_date="-2y")
            # year=date.year
            # month=date.month
            # day=date.day
            if treatment[1]==0: # Case that there's no treatment-fee
                payment="-"
            else:
                payment=random.choice(self.list_payment)
            result = collections.OrderedDict([
                ('name', self.fake.name()),
                ('age', self.fake.pyint(10,100)),
                ('address', self.fake.address()),
                ('hospital', random.choice(self.list_hospital)),
                ('treatment', treatment),
                ('payment', payment),
                ('date', date)
            ])
        return result

# 카프카 서버
bootstrap_servers = ["localhost:9095"]

# 카프카 공급자 생성
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         key_serializer= lambda x: dumps(x).encode('utf-8'),
                         acks=1,
                         #linger_ms=500,
                         value_serializer= lambda x: dumps(x).encode('utf-8')
                        )

# 카프카 토픽
str_topic_name = 'lone-p1r1-5'

#-------Message production with Faker------
#fake = fakeDataGenerator()
for i in range(100):
    #registered_user = get_registered_user()
    #fakedata = fake.gendata()
    producer.send("lone-p1r1-5",key= "foo",value="{\"_id\": {\"$oid\": \"604ad227d644c73281dd784b\"}, \"customerGroupId\": [], \"hospitalId\": \"vatech\", \"id\": \"5520e4e6-b06f-4177-a7a9-3046e6b9523f\", \"address\": \"\", \"birthDate\": {\"$date\": 715577235}, \"cellphoneNumber\": \"+84010348190904\", \"chartNumber\": \"18\", \"consentTo3rdPartyAgreement\": true, \"doctor\": \"bd297784-2fc4-4ff0-bb6d-bdd7beb342d3\", \"email\": \"\", \"grade\": \"\", \"memo\": \"\", \"name\": \"youngho\", \"newOrExistingPatient\": \"1\", \"personalInformationAgreement\": true, \"recommender\": \"a12d99b2-c41f-403e-b146-cded5317dd59\", \"sex\": \"1\" ")
    #producer.send("lone-p1r1-2",key= "name",value="Aram")
    #producer.send("lone-p1r1-2",key= "address",value="Daejeon")
    # response = producer.send(str_topic_name,
    #                          fakedata2
    #                         ).add_callback(on_send_success).add_errback(on_send_error)
    #time.sleep(0.5)
     