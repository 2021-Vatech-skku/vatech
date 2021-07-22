from pyspark.sql import SparkSession
import time

if __name__=="__main__":
    
    spark=SparkSession.builder.appName("etl process").getOrCreate()
    start= time.time()
    df = spark.read.format("json").load("/Users/baekwoojeong/Documents/pyspark/fakeData/modified_data")
    df.coalesce(1).write.format("json").mode("overwrite").save("test_json")
    print("(json) time :", time.time() -start)

    