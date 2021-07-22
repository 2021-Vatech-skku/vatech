from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import *
from pyspark.sql.functions import udf, col, from_json, flatten, explode, count
from datetime import datetime
import argparse

def getChart(df):
    df=df.withColumn("patient_ID",df["patient.patientID"])
    df=df.withColumn("patient_age",df["patient.age"])
    df=df.withColumn("patient_sex",df["patient.sex"])
    df=df.withColumn("year",df["visit.date.year"])
    df=df.withColumn("month",df["visit.date.month"])
    df=df.withColumn("day",df["visit.date.day"])
    df=df.withColumn("hospital_name",df["hospital.hospitalID"])
    df=df.withColumn("treatment_name",df["treatment.name"])
    df = df.select(
        df["patient_ID"],
        df["patient_age"],
        df["patient_sex"],
        df["hospital_name"],
        df["doctor"],
        df["treatment_name"],
        df["year"],
        df["month"],
        df["day"],
    ).orderBy("patient", ascending=False)
    return df

def getReceipt(df):
    df=df.withColumn("hospital_name",df["hospital.hospitalID"])
    df=df.withColumn("hospital_address",df["hospital.address"])
    df=df.withColumn("hospital_contact",df["hospital.contact"])
    df=df.withColumn("year",df["visit.date.year"])
    df=df.withColumn("month",df["visit.date.month"])
    df=df.withColumn("day",df["visit.date.day"])
    df=df.withColumn("patient_ID",df["patient.patientID"])
    df=df.withColumn("treatment_name",df["treatment.name"])
    df=df.withColumn("treatment_price",df["treatment.price"])
    df = df.select(
        df["hospital_name"],
        df["hospital_address"],
        df["hospital_contact"],
        df["year"],
        df["month"],
        df["day"],
        df["patient_ID"],
        df["treatment_name"],
        df["treatment_price"],
        df["payment"],
    ).orderBy("patient", ascending=False)
    return df

if __name__=="__main__":
    spark=SparkSession.builder.appName("etl process").getOrCreate()    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="target info", default="chart")
    parser.add_argument("-if","--inputformat", help="input format", default="json")
    parser.add_argument("-of", "--outputformat", help="output format", default="parquet")
    parser.add_argument("-o", "--output", help="output path", default="parquet")
    args = parser.parse_args()

    df = spark.read.format(args.inputformat).load("/Users/baekwoojeong/Documents/pyspark/fakeData/data")
    spark.sparkContext.setLogLevel("ERROR")
    print("original data")
    df.printSchema()
    df.show(50)

    if args.target == "chart":
        df = getChart(df)
        df_sum = df.groupBy("doctor").agg(count("patient_ID")).withColumnRenamed("count(patient_ID)", "patient_num")
    elif args.target == "receipt":
        df = getReceipt(df)
        df_sum = df.groupBy("hospital_name").sum("treatment_price").withColumnRenamed("sum(treatment_price)", "profit")\
            .withColumnRenamed("hospital_name", "hospital")
            
    df.printSchema()
    df.show(50)
    df_sum.printSchema()
    df_sum.show(50, truncate=False)
    
    df.coalesce(1).write.format(args.outputformat).mode("overwrite").save(args.output)