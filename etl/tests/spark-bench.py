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
        spark = SparkSession.builder.appName("Data Read Benchmark").getOrCreate()
        df = spark.read.format(dataType).option("header", "true").load("./parsed/" + dataType)
        spark.sparkContext.setLogLevel("ERROR")
        start_time = timeit.default_timer()
        print("Original Data")
        df.show()
        end_time = timeit.default_timer() 
        df = df.sort(desc("patient_name"), "date") # SQL을 이용한 정렬
        print("Sort by patient_name and date")
        df.show()
        print("Groupby patient_name, sum of price")
        df.groupBy("patient_name").sum("price").show() # filter
        df.printSchema()
        print(dataType.upper() + " : " + str(end_time - start_time))
        # remove data
        # add data

