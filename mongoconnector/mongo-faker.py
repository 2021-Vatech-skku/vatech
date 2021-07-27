#from _typeshed import Self
from copy import Error
from pymongo import MongoClient, InsertOne
from faker import Faker
import collections
import timeit
import time
from datetime import datetime
import logging
import argparse
import random


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
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--mongodb",
        help="mongodb url",
        default="mongo.it.vsmart00.com",
    )

    parser.add_argument(
        "-p",
        "--port",
        help="port",
        default=27017,
    )
    args = parser.parse_args()

    print('connect to mongo.. {} {}'.format(args.mongodb, int(args.port)))
    client = MongoClient(args.mongodb, 
                         port=int(args.port),
                         username='haruband',
                         password='haru1004',
    )
    print(client.server_info())
    print('connection established')
    db = client['jee']
    print('loaded db \'jee\'')
    N = 100
    fake = fakeDataGenerator()
    ts0 = timeit.default_timer()
    print('writing..')
    doc = []
    for i in range(N):
        doc.append(InsertOne(fake.gendata()))
    col = db['patients']
    col.bulk_write(doc)
    ts1 = timeit.default_timer()
    print("runtime = {}".format(ts1 - ts0))
