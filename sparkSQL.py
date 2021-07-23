import os
from pyspark.sql import *
from pyspark.sql.types import *
from delta.tables import *

WAREHOUSE_PATH = os.environ.get("SPARK_HOME") + "/spark-warehouse"

spark = SparkSession.builder.appName("Query Through Thrift JDBC Server")\
  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
  .config("hive.metastore.uris", "jdbc:hive2://localhost:10000/default")\
  .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
  # .config("spark.sql.warehouse.dir", WAREHOUSE_PATH)\

df = spark.read.format("parquet").load("./parsed/parquet")
db_url = "jdbc:hive2://localhost:10000/"

print("Parsed Data")
df.show()
df.printSchema()

df.createOrReplaceTempView("thirt")
spark.sql("select * from thirt").show()

df.write.format("delta").mode("overwrite").save("delta")
