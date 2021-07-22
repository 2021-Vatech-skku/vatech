from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

if __name__ == "__main__":
  
  sc = SparkContext(appName="CSV2Parquet")
  sqlContext = SQLContext(sc)
  
  schema = StructType([
           StructField("name", StringType(), True),
           StructField("age", IntegerType(), True),
           StructField("job", StringType(), True)])
  
  spark=SparkSession.builder.appName("pyspark csv to parquet").getOrCreate()
  
  df=spark.read.csv("/Users/baekwoojeong/Documents/pyspark/convert/people.csv", header=True, schema=schema)
  df.write.parquet("/Users/baekwoojeong/Documents/pyspark/convert/people.parquet")


