import os
from pyspark.sql import *
from pyspark.sql.types import *
from delta.tables import *

WAREHOUSE_PATH = os.environ.get("SPARK_HOME") + "/spark-warehouse"

spark = SparkSession.builder.appName("Query Through Thrift JDBC Server")\
  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
  .config("hive.metastore.uris", "jdbc:hive2://localhost:10000/default")\
  .config("spark.hadoop.fs.s3a.access.key", "haruband")\
  .config("spark.hadoop.fs.s3a.secret.key", "haru1004")\
  .config("spark.hadoop.fs.s3a.path.style.access", "true")\
  .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
  .config("spark.hadoop.fs.s3a.endpoint", "http://minio.it.vsmart00.com")\
  .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.format("parquet").load("./parsed/parquet")
db_url = "jdbc:hive2://localhost:10000/"

print("Parsed Data")
df.show()
df.printSchema()

df.createOrReplaceTempView("thirt")
spark.sql("select * from thirt").show()

df.write.format("delta").save("s3a://songhyun/test")
