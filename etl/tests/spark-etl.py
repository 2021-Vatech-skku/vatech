import timeit
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, desc, col

txschema = StructType([
    StructField("treat_name", StringType(), False),
    StructField("price", LongType(), False)
])

ptschema = StructType([
    StructField("uuid4", StringType(), False),
    StructField("patient_name", StringType(), False),
    StructField("age", IntegerType(), False),
    StructField("sex", StringType(), False)
])

dcschema = StructType([
    StructField("clinic_name", StringType(), False),
    StructField("address", StringType(), False),
    StructField("telephone", StringType(), False)
])


if __name__ == "__main__":
    dataType = "json"
    spark = SparkSession.builder.appName(
        "ETL Using SparkSQL example").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR") # This option don't print any INFO messages on console
    df = spark.read.format(dataType).option(
        "header", "true").load("./data." + dataType)
    print("Original Data")
    df.show()  # 원래 데이터 형
    df.printSchema()
    df = df.withColumn("content", from_json("content", txschema))
    df = df.withColumn("patient", from_json("patient", ptschema))
    df = df.withColumn("dental_clinic", from_json("dental_clinic", dcschema))
    print("JSON Paresd Data")
    df.show()  # json 문자열 parse
    df = df.select("date", "payment", "content.*", "patient.*", "dentist", "dental_clinic.*")  # json 데이터 읽기
    print("All Useful Data")
    df.show()
    df.write.format("json").mode("overwrite").option("header", "true").save("./output/json")
    df = df.groupBy("clinic_name").sum("price").withColumnRenamed("sum(price)", "profit")# 치과별 매출
    df = df.sort(desc("profit")).withColumnRenamed("clinic_name", "dental_clinic")
    print("Dental Clinic Profit")
    df.show()