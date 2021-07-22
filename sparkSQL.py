'''
  1. java -jar metabase.jar
  2. $SPARK_HOME \ ./sbin/start-thriftserver.sh
  3. beeline \ !connect jdbc:hive2://localhost:10000
  4. spark-submit jdbc.py
'''

from pyspark.sql import *
from pyspark.sql.types import *

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

spark = SparkSession.builder.appName("Dataframe to metabase using Thrift JDBC Server")\
  .enableHiveSupport()\
  .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.schema(schema).format("parquet").load("./parsed/parquet")
db_url = "jdbc:hive2://localhost:10000/sql_study"

print("Parsed Data")
df.show()
df.printSchema()

df.write.format("jdbc").option("url", db_url).option("user", "songhyun").option("dbtable", "test").mode("append").save()
# df.write.format("jdbc").option("url", db_url).option("dbtable", "dummy").option("createTableColumnTypes", '''date string, payment string, treat_name string, price BIGINT, uuid4 string, patient_name string, age INTEGER, sex string, dentist string, clinic_name string, address string, telephone string''').save()
