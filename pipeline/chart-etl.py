import os
from datetime import datetime
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, flatten, explode, udf

timetostr = udf(lambda x: datetime.fromtimestamp(x).strftime("%Y%m%d"))

schema = StructType(
    [
      StructField(
          "_id", StructType([StructField("$oid", StringType(), False)]), False
      ),
      StructField("content", StructType([
        StructField("tx", StructType([
          StructField("treatments", ArrayType(StructType([
            StructField("treats", ArrayType(StructType([
              StructField("name", StringType(), False),
              StructField("price", IntegerType(), False)
            ])),False)
          ])), False)
        ]), False)
      ]), False),
      StructField("hospitalId", StringType(), False),
      StructField("date", StructType([StructField("$date", IntegerType(), False)]), False),
      StructField("patient", StringType(), False)
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

df = spark.read.format("json").load("s3a://mongodb/topics/clever.dev0-chart")

df = df.filter(df.operationType == "insert").select("fullDocument")
df = df.withColumn("test", from_json(df.fullDocument, schema)).select("test.*")
df = df.withColumn("content", explode(flatten("content.tx.treatments.treats")))
df = df.withColumn("date", timetostr(df["date.$date"]))
df = df.select(
  df["_id.$oid"].alias("oid"), 
  df["content.name"].alias("name"), 
  df["content.price"].alias("price"), 
  df["hospitalId"].alias("hospital"), 
  "date", 
  "patient"
)

df.show(10, truncate=False)
df.printSchema()
tmp = df.toPandas()
spark.stop()

# Create new sparksession to use another s3 endpoint
sc.set("spark.hadoop.fs.s3a.endpoint", "http://minio.it.vsmart00.com")
spark = SparkSession.builder.appName("Chart ETL").config(conf=sc).getOrCreate()
df = spark.createDataFrame(tmp)
df.coalesce(1).write.format("delta").save("s3a://songhyun/chart")