import os
from datetime import datetime, date
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, flatten, explode, udf

timetostr = udf(lambda x: datetime.fromtimestamp(x).strftime("%Y%m%d") if type(x) is int else None)

schema = StructType(
    [
      StructField("hospitalId", StringType(), False),
      StructField("birthDate", StructType([StructField("$date", IntegerType(), False)]), False),
      StructField("id", StringType(), False),
      StructField("name", StringType(), False),
      StructField("newOrExistingPatient", StringType(), False),
      StructField("sex", StringType(), False),
      StructField("address", StringType(), False),
    ]
)

sc = SparkConf()
sc.set("spark.sql.warehouse.dir", os.environ.get("SPARK_HOME"))
sc.set("spark.hadoop.fs.s3a.access.key", os.environ.get("MINIO_ACCESS_KEY", "haruband"))
sc.set("spark.hadoop.fs.s3a.secret.key", os.environ.get("MINIO_SECRET_KEY", "haru1004"))
sc.set("spark.hadoop.fs.s3a.path.style.access", "true")
sc.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc.set("spark.hadoop.fs.s3a.endpoint", "https://minio.develop.vsmart00.com")

spark = SparkSession.builder.appName("Chart ETL").config(conf=sc).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.format("json").load("s3a://mongodb/topics/clever.dev0-patient")
df = df.filter(df.operationType == "insert").select("fullDocument")
df = df.withColumn("test", from_json(df.fullDocument, schema)).select("test.*")
df = df.withColumn("date", timetostr(df["birthDate.$date"]))
df = df.select(
  df["id"].alias("patient"), 
  df["hospitalId"].alias("hospital"), 
  "sex",
  "name", 
  "address",
  df["date"].alias("birth"), 
  df["newOrExistingPatient"].alias("existing"), 
)

df.show(10, truncate=False)
df.printSchema()
tmp = df.toPandas()
spark.stop()

# Create new sparksession to use another s3 endpoint
sc.set("spark.hadoop.fs.s3a.endpoint", "http://minio.it.vsmart00.com")
spark = SparkSession.builder.appName("Chart ETL").config(conf=sc).getOrCreate()
df = spark.createDataFrame(tmp)
df.coalesce(1).write.format("delta").save("s3a://songhyun/patient")
print("Uploaded to K8S")