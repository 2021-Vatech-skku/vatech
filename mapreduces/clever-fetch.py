import os
import argparse
import json
from datetime import datetime
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import *
from pyspark.sql.functions import col, from_json, last, first
from pyspark.sql.utils import *
from delta.tables import *

from clever import (
    getCleverDocumentID,
    getCleverSchema,
    getCleverTable,
)


def handleDumpOperation(sq, df0):
    def handleDumpFields(doc):
        print(json.dumps(doc, indent=2))

    df0.foreach(handleDumpFields)


def handleInsertOperation(
    sq, df0, coll, schema, partitions, outputformat, outputbucket
):
    df0 = df0.filter(df0.fullDocument.isNotNull())
    df0 = df0.withColumn(
        "document", from_json(col("fullDocument"), getCleverSchema(coll))
    )
    df0 = df0.select(getCleverDocumentID(df0), "document.*")

    df0 = getCleverTable(df0, schema)
    df0.printSchema()
    df0.show(truncate=True)

    if args.partitions:
        df0.write.partitionBy(partitions.split(",")).format(outputformat)\
            .mode("append").save("s3a://{}/{}".format(outputbucket,coll))
    else:
        df0.write.format(outputformat).mode("append").save("s3a://{}/{}".format(outputbucket,coll))
    
    print("insert done!!")


def handleUpdateOperation(
    sq, df0, coll, schema, partitions, outputformat, outputbucket
):
    df0 = df0.filter(df0.fullDocument.isNotNull())
    df0 = df0.withColumn(
        "document", from_json(col("fullDocument"), getCleverSchema(coll))
    )
    df0 = df0.select(getCleverDocumentID(df0), "document.*")
    df0 = df0.groupBy("oid").agg(
        *map(
            lambda x: last(df0[x]).alias(x),
            filter(lambda x: x != "oid", df0.schema.names),
        )
    )

    df0 = getCleverTable(df0, schema)

    df0 = df0.groupBy("oid").agg(
        *map(
            lambda x: last(df0[x]).alias(x),
            filter(lambda x: x != "oid", df0.schema.names),
        )
    )
    df0.show(truncate=False)

    dft = DeltaTable.forPath(sq, "s3a://{}/{}".format(outputbucket,coll))
    dft.alias("origin").merge(df0.alias("update"), "origin.oid = update.oid")\
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    print("update done!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-if",
        "--inputformat",
        help="input format",
        default="json",
    )
    parser.add_argument("-b", "--bucket", help="target bucket", default="skku-sanhak")
    parser.add_argument(
        "-c", "--collection", help="target collection", default="jee.clever.dev0-chart.test"
    )
    parser.add_argument("-y", "--year", help="target year", type=int, default=datetime.today().year)
    parser.add_argument("-m", "--month", help="target month", type=int, default=datetime.today().month)
    parser.add_argument("-d", "--day", help="target day", type=int, default=datetime.today().day)
    parser.add_argument("-t", "--targets", help="output targets", default="insert")
    parser.add_argument("-s", "--schema", help="output schema")
    parser.add_argument("-of", "--outputformat", help="output format", default="delta")
    parser.add_argument("-ob", "--outputbucket", help="output path", default="test")
    parser.add_argument("-p", "--partitions", help="output partitions")
    parser.add_argument(
        "-u",
        "--minio",
        help="minio url",
        default="https://minio.develop.vsmart00.com",
    )
    parser.add_argument(
        "-e",
        "--elasticsearch",
        help="elasticsearch url",
        default="localhost:9200",
    )
    parser.add_argument("-l", "--loglevel", help="log level", default="ERROR")
    args = parser.parse_args()

    sc = SparkConf()
    sc.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    sc.set(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    sc.set(
        "spark.hadoop.fs.s3a.access.key",
        os.environ.get("MINIO_ACCESS_KEY", "haruband"),
    )
    sc.set(
        "spark.hadoop.fs.s3a.secret.key",
        os.environ.get("MINIO_SECRET_KEY", "haru1004"),
    )
    sc.set("spark.hadoop.fs.s3a.path.style.access", "true")
    sc.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    sc.set("spark.hadoop.fs.s3a.endpoint", args.minio)
    sc.set("es.nodes", args.elasticsearch)
    sc.set("es.nodes.discovery", "true")
    sc.set("es.index.auto.create", "true")

    sq = SparkSession.builder.config(conf=sc).appName("clever-fetch").getOrCreate()
    sq.sparkContext.setLogLevel(args.loglevel)

    s3url = "s3a://{}/topics/{}".format(args.bucket, args.collection)
    if args.year > 0:
        s3url = s3url + "/year={:04d}".format(args.year)
        if args.month > 0:
            s3url = s3url + "/month={:02d}".format(args.month)
            if args.day > 0:
                s3url = s3url + "/day={:02d}".format(args.day)
    try:
        df0 = sq.read.format(args.inputformat).load(s3url)
    except AnalysisException:
        print("No Data for {}-{}-{}".format(args.year, args.month, args.day))
        exit(0)

    if "chart" in args.collection:
        coll="chart"
    if "receipt" in args.collection:
        coll="receipt"
    if "patient" in args.collection:
        coll="patient"

    if "dump" in args.targets:
        handleDumpOperation(sq, df0)

    if "insert" in args.targets:
        handleInsertOperation(
            sq,
            df0.filter(df0["operationType"] == "insert"),
            coll,
            args.schema if args.schema else coll,
            args.partitions,
            args.outputformat,
            args.outputbucket,
        )
    if "update" in args.targets:
        handleUpdateOperation(
            sq,
            df0.filter(df0["operationType"] == "update"),
            coll,
            args.schema if args.schema else coll,
            args.partitions,
            args.outputformat,
            args.outputbucket,
        )
