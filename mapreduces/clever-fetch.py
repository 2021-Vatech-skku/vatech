import os
import argparse
import json
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import *
from pyspark.sql.functions import col, from_json, last, first
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
    sq, df0, collection, schema, partitions, outputformat, output
):
    df0 = df0.filter(df0.fullDocument.isNotNull())
    df0 = df0.withColumn(
        "document", from_json(col("fullDocument"), getCleverSchema(collection))
    )
    df0 = df0.select(getCleverDocumentID(df0), "document.*")

    df0 = getCleverTable(df0, schema)
    df0.show(truncate=True)

    if args.partitions:
        df0.write.partitionBy(partitions.split(",")).format(outputformat).mode(
            "append"
        ).save(output)
    else:
        df0.write.format(outputformat).mode("append").save(output)


def handleUpdateOperation(
    sq, df0, collection, schema, partitions, outputformat, output
):
    df0 = df0.filter(df0.fullDocument.isNotNull())
    df0 = df0.withColumn(
        "document", from_json(col("fullDocument"), getCleverSchema(collection))
    )
    df0 = df0.select(getCleverDocumentID(df0), "document.*")
    df0 = df0.groupBy("oid").agg(
        *map(
            lambda x: last(df0[x]).alias(x),
            filter(lambda x: x != "oid", df0.schema.names),
        )
    )

    df0 = getCleverTable(df0, schema)
    df0.show(truncate=False)

    dft = DeltaTable.forPath(sq, output)
    dft.alias("origin").merge(
        df0.alias("update"), "origin.oid = update.oid"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-if",
        "--inputformat",
        help="input format",
        default="json",
    )
    parser.add_argument("-b", "--bucket", help="target bucket", default="mongodb")
    parser.add_argument(
        "-c", "--collection", help="target collection", default="clever.dev0-chart"
    )
    parser.add_argument("-y", "--year", help="target year", type=int, default=0)
    parser.add_argument("-m", "--month", help="target month", type=int, default=0)
    parser.add_argument("-d", "--day", help="target day", type=int, default=0)
    parser.add_argument("-t", "--targets", help="output targets", default="insert")
    parser.add_argument("-s", "--schema", help="output schema")
    parser.add_argument("-of", "--outputformat", help="output format", default="delta")
    parser.add_argument("-o", "--output", help="output path", default="delta")
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

    df0 = sq.read.format(args.inputformat).load(s3url)
    '''
    df0.printSchema()
    df0 = df0.filter(df0["operationType"] == "insert")
    df0 = df0.withColumn(
        "document", from_json(col("fullDocument"), getCleverSchema(args.collection))
    )
    df0 = df0.select("document.*")
    df0.printSchema()

    if args.target == "treats":
        df0 = getCleverChartTreats(df0)
        name_list = [(row.name) for row in df0.select("name").collect()]
        price_dic = {
            row.name: row.price for row in df0.select("name", "price").collect()
        }
        df0 = genFakeChartData(df0, name_list, price_dic)
    elif args.target == "receipt":
        df0 = getCleverReceipts(df0)
        exiting_dic = {row.patient: 2 for row in df0.select("patient").collect()}
        df0 = genFakeReceiptData(df0, exiting_dic)
    df0.printSchema()
    df0.show(truncate=False)
    name_list = [(row.name) for row in df0.select("name").collect()]

    #df0.orderBy("date",ascending=False).show(truncate=False)
    print(df0.count())
    if args.partitions:
        df0.coalesce(1).write.partitionBy(args.partitions.split(",")).format(
            args.outputformat
        ).mode("overwrite").save(args.output)
    else:
        df0.coalesce(1).write.format(args.outputformat).mode("overwrite").save(
            args.output
        )
    '''

    if "dump" in args.targets:
        handleDumpOperation(sq, df0)

    if "insert" in args.targets:
        handleInsertOperation(
            sq,
            df0.filter(df0["operationType"] == "insert"),
            args.collection,
            args.schema if args.schema else args.collection,
            args.partitions,
            args.outputformat,
            args.output,
        )
    if "update" in args.targets:
        handleUpdateOperation(
            sq,
            df0.filter(df0["operationType"] == "update"),
            args.collection,
            args.schema if args.schema else args.collection,
            args.partitions,
            args.outputformat,
            args.output,
        )
