import time
import timeit

from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import udf, col, from_json, flatten, explode, desc, count
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
    sc = SparkContext("local","etl")
    spark=SparkSession.builder.appName("etl process").getOrCreate()
    spark.SparkContext.setLogLevel("ERROR")
    schema = StructType([
             StructField("patient", StructType([
                 StructField("patientID", StringType(), True), StructField("age", IntegerType(), True), StructField("sex", StringType(), True)]), True),
             StructField("doctor", StringType(), True),
             StructField("hospital", StructType([
                 StructField("hospitalID", StringType(), True), StructField("address", StringType(), True), StructField("contact", StringType(), True)]), True),
             StructField("treatment", StructType([
                 StructField("name", StringType(), True), StructField("price", IntegerType(), True)]), True),
             StructField("visit", StructType([
                 StructField("date", StructType([
                     StructField("year", IntegerType(), True), StructField("month", IntegerType(), True), StructField("day", IntegerType(), True)]), True)]), True),
             StructField("payment", StringType(), True)])

# add argument rules
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="target info", default="chart")
    parser.add_argument("-if","--inputformat", help="input format", default="json")
    parser.add_argument("-of", "--outputformat", help="output format", default="parquet")
    parser.add_argument("-o", "--output", help="output path", default="parquet")
    args = parser.parse_args()
    
    df = spark.read.format(args.inputformat).load("./data")
    spark.sparkContext.setLogLevel("ERROR")
    print("Original Data")
    df.show(50)
    df.printSchema()

    if args.target == "chart":
        df = getChart(df)
        df1 = df.groupBy("doctor").agg(count("patient_ID")).withColumnRenamed("count(patient_ID)", "patient_num")
        # 의사별 환자 수
    elif args.target == "receipt":
        df = getReceipt(df)
        df1 = df.groupBy("hospital_name").sum("treatment_price").withColumnRenamed("sum(treatment_price)", "profit").\
          withColumnRenamed("hospital_name", "hospital")
        # 병원별 수익
        print("Hospital Profit")

    print("Parsed Data")
    df.show(50)
    df.printSchema()

    print("Filtered Data")
    df1.show(50)
    df1.printSchema()
    
    # Save ETL data
    df.coalesce(1).write.format(args.outputformat).option("header", "true").mode("overwrite").save(args.output)
