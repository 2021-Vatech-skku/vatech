
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, desc, col

if __name__ == "__main__":
  origin = "json"
  origin_path = "./data/data." + origin
  convertType = "parquet"
  convert_path = "./output/" + convertType
  spark = SparkSession.builder.appName("Data Conversion").getOrCreate()
  df = spark.read.format(origin).option("header", "true").load(origin_path) # load orinial file
  df.write.format(convertType).mode("overwrite").option("header", "true").save(convert_path) # convert to parquet, json, csv
