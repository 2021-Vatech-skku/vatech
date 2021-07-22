from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark import SparkContext

if __name__=="__main__":
    url = "mongo.it.vsmart00.com"
    database = "sample3"
    collection = "profile3"
    username = "haruband"
    password = "haru1004"

    conf = SparkConf().setAll([('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')])

    spark = SparkSession.builder.appName("save to mongo") \
    .config("spark.mongodb.input.uri", "mongodb://{}/{}.{}".format(url, database, collection))\
    .config("spark.mongodb.output.uri", "mongodb://{}/{}.{}".format(url, database, collection))\
    .config(conf=conf).getOrCreate()

    df = spark.read.format("json").load("/Users/baekwoojeong/documents/pyspark/database/profile")
    spark.sparkContext.setLogLevel("ERROR")
    df.printSchema()
    df.show(50)
    #print("almost~")
    
    df.coalesce(1).write.format("mongo").mode("append") \
        .option("spark.mongodb.output.uri", "mongodb://{}:{}@{}/{}.{}?authSource=admin".format(username, password, url, database, collection))\
        .save()
    #print("done!!")