import json
from datetime import datetime
from pyspark.sql.types import *
from pyspark.sql.functions import udf, col, from_json, flatten, explode


uTimestampToDate = udf(
    lambda d: datetime.fromtimestamp(d).strftime("%Y%m%d") if type(d) is int else None
)

uDocumentKeyToID = udf(lambda d: json.loads(d)["_id"]["$oid"])


def getCleverDocumentID(df0):
    return uDocumentKeyToID(df0["documentKey"]).alias("oid")


def getCleverSchema(collection):
    if collection.endswith("chart"):
        trSchema = StructType(
            [
                StructField("name", StringType(), False),
                StructField("price", IntegerType(), False),
            ]
        )
        tmSchema = StructType(
            [
                StructField(
                    "treats",
                    ArrayType(
                        trSchema,
                        False,
                    ),
                    False,
                ),
            ]
        )
        txSchema = StructType(
            [
                StructField(
                    "treatments",
                    ArrayType(
                        tmSchema,
                        False,
                    ),
                    False,
                )
            ]
        )
        schema = StructType(
            [
                StructField("hospitalId", StringType(), False),
                StructField("patient", StringType(), False),
                StructField("type", StringType(), False),
                StructField(
                    "date", StructType([StructField("$date", IntegerType(), False)])
                ),
                StructField(
                    "content", StructType([StructField("tx", txSchema, False)]), False
                ),
                StructField("lastModifiedTime", IntegerType(), False),
            ]
        )
        return schema
    elif collection.endswith("receipt"):
        schema = StructType(
            [
                StructField("hospitalId", StringType(), False),
                StructField("patient", StringType(), False),
                StructField(
                    "receiptDate",
                    StructType([StructField("$date", IntegerType(), False)]),
                ),
                StructField("status", StringType(), False),
                StructField("newOrExistingPatient", StringType(), False),
                StructField("lastModifiedTime", IntegerType(), False),
            ]
        )
        return schema
    elif collection.endswith("patient"):
        schema = StructType(
            [
                StructField("_id", StringType(), True),
                StructField("id", StringType(), True),
                StructField("hospitalId", StringType(), True),
                StructField("sex", StringType(), True),
                StructField("name", StringType(), True),
                StructField("address", StringType(), True),
                StructField("birthDate",TimestampType(),True),
                StructField("newOrExistingPatient", StringType(), True),
                StructField("lastModifiedTime", IntegerType(), False),
            ]
        )
        return schema


def getCleverTable(df0, coll):
    if coll.endswith("chart"):
        df0 = df0.filter(df0["type"] == "TX")
        df0 = df0.withColumn("date", uTimestampToDate(df0["date.$date"]))
        df0 = df0.withColumn(
            "treats", explode(flatten(df0["content.tx.treatments.treats"]))
        )
        df0 = df0.withColumn("name", df0["treats.name"])
        df0 = df0.withColumn("price", df0["treats.price"])
        df0 = df0.select(
            df0["oid"],
            df0["date"],
            df0["hospitalId"].alias("hospital"),
            df0["patient"],
            df0["name"],
            df0["price"],
        ).orderBy("date", ascending=False)
    elif coll.endswith("receipt"):
        df0 = df0.withColumn("date", uTimestampToDate(df0["receiptDate.$date"]))
        df0 = df0.select(
            df0["oid"],
            df0["date"],
            df0["hospitalId"].alias("hospital"),
            df0["patient"],
            df0["newOrExistingPatient"].alias("existing"),
        ).orderBy("date", ascending=False)
    elif coll.endswith("patient"):
        df0 = df0.withColumn("birth", uTimestampToDate(df0["birthDate"]))
        df0 = df0.withColumn("oid", uTimestampToDate(df0["_id"]))
        df0 = df0.select(
            df0["oid"],
            df0["id"].alias("patient"),
            df0["hospitalId"].alias("hospital"),
            df0["sex"],
            df0["name"],
            df0["address"],
            df0["birth"],
            df0["newOrExistingPatient"].alias("existing"),
        )
    return df0