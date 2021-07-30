import os
import argparse
from datetime import datetime, date
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, udf, last

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
      StructField("lastModifiedTime", IntegerType(), False),
    ]
)

sc = SparkConf()
sc.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
sc.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
sc.set("spark.sql.warehouse.dir", os.environ.get("SPARK_HOME"))
sc.set("spark.hadoop.fs.s3a.access.key", os.environ.get("MINIO_ACCESS_KEY", "haruband"))
sc.set("spark.hadoop.fs.s3a.secret.key", os.environ.get("MINIO_SECRET_KEY", "haru1004"))
sc.set("spark.hadoop.fs.s3a.path.style.access", "true")
sc.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc.set("spark.hadoop.fs.s3a.endpoint", "https://minio.develop.vsmart00.com")

spark = SparkSession.builder.appName("Patient ETL").config(conf=sc).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

url = "s3a://mongodb/topics/clever.dev0-patient"
mode = "overwrite"
parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", help="target year", type=int, default=0)
parser.add_argument("-m", "--month", help="target month", type=int, default=0)
parser.add_argument("-d", "--day", help="target day", type=int, default=0)
args = parser.parse_args()
url = "s3a://mongodb/topics/clever.dev0-patient"
if args.year > 0:
  url = url + "/year={:04d}".format(args.year)
  if args.month > 0:
    url = url + "/month={:02d}".format(args.month)
    if args.day > 0:
      url = url + "/day={:02d}".format(args.day)
      mode = "append"

df = spark.read.format("json").load(url)

# append
df0 = df.filter(df.operationType == "insert").select("fullDocument")
df0 = df0.withColumn("test", from_json(df0.fullDocument, schema)).select("test.*")
df0 = df0.withColumn("date", timetostr(df0["birthDate.$date"]))
df0 = df0.select(
  df0["id"].alias("patient"), 
  df0["hospitalId"].alias("hospital"), 
  df0["sex"],
  df0["name"], 
  df0["address"],
  df0["date"].alias("birth"), 
  df0["newOrExistingPatient"].alias("existing"), 
)
df0.show(10, truncate=True)
df0.coalesce(1).write.format("delta").mode(mode).save("s3a://test/sh/patient")

# update
df1 = df.filter(df.operationType == "update").select("fullDocument")
df1 = df1.withColumn("test", from_json(df1.fullDocument, schema)).select("test.*")
df1 = df1.sort("lastModifiedTime").groupBy(df1["id"]).agg(
  *map(
    lambda x: last(df1[x]).alias(x),
    filter(lambda x: x != "id", df1.schema.names),
  )
)
df1 = df1.withColumn("date", timetostr(df1["birthDate.$date"]))
df1 = df1.select(
  df1["id"].alias("patient"), 
  df1["hospitalId"].alias("hospital"), 
  df1["sex"],
  df1["name"], 
  df1["address"],
  df1["date"].alias("birth"), 
  df1["newOrExistingPatient"].alias("existing"), 
)
df1.show(10, truncate=True)

df = spark.read.format("delta").load("s3a://test/sh/patient")
df = df.join(df1, df["patient"] == df1["patient"], "leftanti")
df2 = df.union(df1)
df2.coalesce(1).write.format("delta").mode("overwrite").save("s3a://test/sh/patient")
print("Uploaded.")

'''
tmp = df.toPandas()
spark.stop()

# Create new sparksession to use another s3 endpoint
sc.set("spark.hadoop.fs.s3a.endpoint", "http://minio.it.vsmart00.com")
spark = SparkSession.builder.appName("Patient ETL").config(conf=sc).getOrCreate()
df = spark.createDataFrame(tmp)
df.coalesce(1).write.format("delta").mode("overwrite").save("s3a://songhyun/patient")
print("Uploaded to K8S")
'''