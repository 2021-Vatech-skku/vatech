import timeit
import argparse
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, desc, col

txschema = StructType([
    StructField("treat_name", StringType(), False),
    StructField("price", LongType(), False)
])

ptschema = StructType([
    StructField("uuid4", StringType(), False),
    StructField("patient_name", StringType(), False),
    StructField("age", IntegerType(), False),
    StructField("sex", StringType(), False)
])

dcschema = StructType([
    StructField("clinic_name", StringType(), False),
    StructField("address", StringType(), False),
    StructField("telephone", StringType(), False)
])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-if", "--inputformat", help="input format", default="json")
    args = parser.parse_args()
    
    iteration = 1
    dataType = args.inputformat
    for i in range(0, iteration):
        spark = SparkSession.builder.appName("Parse original data").getOrCreate()
        df = spark.read.format(dataType).option("header", "true").load("./data/" + dataType)
        print("Original Data")
        df.show()
        spark.sparkContext.setLogLevel("ERROR")
        df = df.withColumn("content", from_json("content", txschema))
        df = df.withColumn("patient", from_json("patient", ptschema))
        df = df.withColumn("dental_clinic", from_json("dental_clinic", dcschema))
        df = df.select("date", "payment", "content.*", "patient.*", "dentist", "dental_clinic.*")
        print("Parsed Data")
        df.show() 