#!/bin/bash

HADOOP_VERSION=${HADOOP_VERSION:-3.2.0}
DELTALAKE_VERSION=${DELTALAKE_VERSION:-1.0.0}
SPARK_SQL_KAFKA_VERSION=${SPARK_SQL_KAFKA_VERSION:-3.1.2}
MONGODB_CONNECTOR_VERSION=${MONGODB_CONNECTOR_VERSION:-3.0.1}

spark-submit \
    --packages org.apache.hadoop:hadoop-aws:${HADOOP_VERSION},io.delta:delta-core_2.12:${DELTALAKE_VERSION},org.apache.spark:spark-sql-kafka-0-10_2.12:${SPARK_SQL_KAFKA_VERSION},org.mongodb.spark:mongo-spark-connector_2.12:${MONGODB_CONNECTOR_VERSION} \
    $@