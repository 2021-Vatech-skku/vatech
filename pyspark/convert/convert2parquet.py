import re
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

if __name__ == "__main__":
  sc = SparkContext("local","PySpark Word Count Exmaple")

  words = sc.textFile("/Users/baekwoojeong/Documents/pyspark/wordCount/input.txt")\
					.map(lambda line: line.lower()).flatMap(lambda line: line.split(" "))\
					.map(lambda word: re.sub(r"[^a-zA-Z0-9]", "", word))
					
  wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)

  spark=SparkSession.builder.appName("pyspark csv to parquet").getOrCreate()	
  schema = StructType([
          StructField("word", StringType(), True),
          StructField("count", IntegerType(), True)])

  df= spark.createDataFrame(data=wordCounts,schema=schema)
  df.show()

 #df.write.option("header","true").csv("/Users/baekwoojeong/Documents/pyspark/convert/wordCount.csv")
 #df.write.option("header","true").json("/Users/baekwoojeong/Documents/pyspark/convert/wordCount.json")
  df.write.option("header","true").parquet("/Users/baekwoojeong/Documents/pyspark/convert/wordCount.parquet")


