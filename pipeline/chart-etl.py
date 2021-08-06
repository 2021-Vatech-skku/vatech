import os
import json
import argparse
from datetime import datetime, date
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, flatten, explode, udf, last

timetostr = udf(lambda x: datetime.fromtimestamp(x).strftime("%Y%m%d") if type(x) is int else None)
documentKeytoOid = udf(lambda d: json.loads(d)["_id"]["$oid"])

schema = StructType(
    [
      StructField(
          "documentKey", StructType([StructField("$oid", StringType(), False)]), False
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
      StructField("patient", StringType(), False),
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

spark = SparkSession.builder.appName("Chart ETL").config(conf=sc).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

mode = "overwrite"
parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", help="target year", type=int, default=0)
parser.add_argument("-m", "--month", help="target month", type=int, default=0)
parser.add_argument("-d", "--day", help="target day", type=int, default=0)
args = parser.parse_args()
url = "s3a://skku-sanhak/topics/jee.clever.dev0-chart.test"
if args.year > 0:
  url = url + "/year={:04d}".format(args.year)
  if args.month > 0:
    url = url + "/month={:02d}".format(args.month)
    if args.day > 0:
      url = url + "/day={:02d}".format(args.day)
      mode = "append"

df = spark.read.format("json").load(url)

# append
df0 = df.filter(df.operationType == "insert").select("documentKey", "fullDocument")
df0 = df0.withColumn("oid", documentKeytoOid(df0["documentKey"]))
df0 = df0.withColumn("test", from_json(df0.fullDocument, schema)).select("oid", "test.*")
df0 = df0.withColumn("content", explode(flatten("content.tx.treatments.treats")))
df0 = df0.withColumn("date", timetostr(df0["date.$date"]))
df0 = df0.select(
  df0["oid"], 
  df0["content.name"].alias("name"), 
  df0["content.price"].alias("price"), 
  df0["hospitalId"].alias("hospital"), 
  df0["date"], 
  df0["patient"],
)
df0.show(10, truncate=True)
df0.coalesce(1).write.format("delta").mode(mode).save("s3a://test/sh/chart")

# Update
df1 = df.filter(df.operationType == "update").select("documentKey", "fullDocument")
df1 = df1.withColumn("oid", documentKeytoOid(df1["documentKey"]))
df1 = df1.withColumn("test", from_json(df1.fullDocument, schema)).select("oid", "test.*")
df1 = df1.sort("lastModifiedTime").groupBy(df1["oid"]).agg(
  *map(
    lambda x: last(df1[x]).alias(x),
    filter(lambda x: x != "oid", df1.schema.names),
  )
)
df1 = df1.withColumn("content", explode(flatten("content.tx.treatments.treats")))
df1 = df1.withColumn("date", timetostr(df1["date.$date"]))
df1 = df1.select(
  df1["oid"], 
  df1["content.name"].alias("name"), 
  df1["content.price"].alias("price"), 
  df1["hospitalId"].alias("hospital"), 
  df1["date"], 
  df1["patient"],
)
df1.show(10, truncate=True)

df = spark.read.format("delta").load("s3a://test/sh/chart")
df = df.join(df1, df["oid"] == df1["oid"], "leftanti")
df2 = df.union(df1)
df2.coalesce(1).write.format("delta").mode("overwrite").save("s3a://test/sh/chart")
df2.show(df2.count())
print("Uploaded.")