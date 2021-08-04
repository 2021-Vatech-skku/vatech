# spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 mongo.py

from pyspark.sql import SparkSession
from pyspark import SparkContext
import timeit

url = "localhost"
port = "27017"
database = "test"
collection = "coll"
username = "haruband"
password = "haru1004"

spark = SparkSession.builder\
  .appName("Mysql JDBC")\
  .config("spark.mongodb.input.uri", "mongodb://{}:{}/{}.{}".format(url, port, database, collection))\
  .config("spark.mongodb.output.uri", "mongodb://{}:{}/{}.{}".format(url, port, database, collection))\
  .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

mongo = spark.read.format("parquet").load("./parsed/parquet")
mongo.show()

start = timeit.default_timer()

mongo.write.format("com.mongodb.spark.sql.DefaultSource")\
  .option("spark.mongodb.output.uri", "mongodb://{}:{}/{}.{}".format(url, port, database, collection))\
  .mode("overwrite")\
  .save()

end = timeit.default_timer()

print(str(end - start) + " time.")