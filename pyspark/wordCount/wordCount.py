#edited
import sys
from pyspark import SparkContext, SparkConf
 
if __name__ == "__main__":
	
	# create Spark context with necessary configuration
	sc = SparkContext("local","PySpark Word Count Exmaple")
	
	# read data from text file and split each line into words
	words = sc.textFile("/Users/baekwoojeong/Documents/pyspark/wordCount/input.txt")\
					.flatMap(lambda line: line.split(" ")).flatMap(lambda line: line.split(";"))\
					.flatMap(lambda line: line.split(".")).flatMap(lambda line: line.split(","))\
					.map(lambda line: line.lower()).filter(lambda x:x!='')

	# count the occurrence of each word
	wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)
	
	# save the counts to output
	wordCounts.saveAsTextFile("/Users/baekwoojeong/Documents/pyspark/wordCount/output/")
