import os
import argparse
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *

from clever import getCleverSchema, getCleverPatients


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--url", help="mongodb url", default="mongodb.develop.vsmart00.com"
    )
    parser.add_argument("-p", "--port", help="mongodb port", type=int, default=15443)
    parser.add_argument("--username", help="mongodb username", default="haruband")
    parser.add_argument("--password", help="mongodb password", default="kk3249")
    parser.add_argument("--database", help="mongodb database", default="clever")
    parser.add_argument(
        "--collection", help="mongodb collection", default="dev0-patient"
    )
    parser.add_argument("-of", "--outputformat", help="output format", default="delta")
    parser.add_argument("-o", "--output", help="output path", default="delta")
    parser.add_argument(
        "-m",
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

    sq = (
        SparkSession.builder.appName("mongodb-fetch")
        .config(
            "spark.hadoop.fs.s3a.access.key",
            os.environ.get("MINIO_ACCESS_KEY", "haruband"),
        )
        .config(
            "spark.hadoop.fs.s3a.secret.key",
            os.environ.get("MINIO_SECRET_KEY", "haru1004"),
        )
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.endpoint", args.minio)
        .config("es.nodes", args.elasticsearch)
        .config("es.nodes.discovery", "true")
        .getOrCreate()
    )
    sq.sparkContext.setLogLevel(args.loglevel)

    df0 = (
        sq.read.format("com.mongodb.spark.sql.DefaultSource")
        .option(
            "spark.mongodb.input.uri",
            "mongodb://{}:{}@{}:{}/{}.{}?authSource=admin&authMechanism=SCRAM-SHA-256&ssl=true".format(
                args.username,
                args.password,
                args.url,
                args.port,
                args.database,
                args.collection,
            ),
        )
        .schema(getCleverSchema(args.collection))
        .load()
    )

    if args.collection.endswith("patient"):
        df0 = getCleverPatients(df0)

    df0.show(truncate=False)

    df0.coalesce(1).write.format(args.outputformat).mode("overwrite").save(args.output)