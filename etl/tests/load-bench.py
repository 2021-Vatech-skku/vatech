import timeit
import time
import argparse
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, desc, col

schema = StructType([
  StructField("date", StringType(), False),
  StructField("payment", StringType(), False),
  StructField("treat_name", StringType(), False),
  StructField("price", LongType(), False),
  StructField("uuid4", StringType(), False),
  StructField("patient_name", StringType(), False),
  StructField("age", IntegerType(), False),
  StructField("sex", StringType(), False),
  StructField("dentist", StringType(), False),
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
        spark = SparkSession.builder.appName("Data Load Benchmark").getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        df = spark.read.format(dataType).option("header", "true").schema(schema).load("./parsed/" + dataType)
        df.show()
        df.printSchema()
        # remove data
        # add data

        # start_time = timeit.default_timer()
        # end_time = timeit.default_timer() # filter(advanced)
        # print(dataType.upper() + " : " + str(end_time - start_time))
