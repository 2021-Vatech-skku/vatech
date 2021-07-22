from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import SparkSession

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("job", StringType(), True)])

spark=SparkSession.builder.appName("pyspark csv read").getOrCreate()

spark.read.csv("/Users/baekwoojeong/Documents/pyspark/convert/people.csv", header=True, schema=schema).show()
