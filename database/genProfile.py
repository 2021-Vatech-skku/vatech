from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import *
from pyspark.sql.functions import *
from datetime import datetime
from faker import Faker
import random
import argparse

if __name__=="__main__":
    sc = SparkContext("local","fake data")
    spark=SparkSession.builder.appName("generate fake profile").getOrCreate()

    fake=Faker()

    tmp=[]
    for i in range(100000):
        tmp.append(fake.profile())
    fakeData=spark.createDataFrame(data=tmp).select('name','sex','birthdate','blood_group','job','mail')
    fakeData.printSchema()
    fakeData.show(50)

    fakeData.coalesce(1).write.format("json").mode("overwrite").save("profile")