from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

# initialise sparkContext
spark=SparkSession.builder.appName("pyspark parquet read").getOrCreate()

sc = spark.sparkContext
sqlContext = SQLContext(sc)

# to read parquet file
df = sqlContext.read.parquet("/Users/baekwoojeong/documents/pyspark/convert/people.parquet")
df.show()
