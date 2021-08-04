#!/bin/bash

# Connector versions
MONGODB_CONNECTOR_VERSION=${MONGODB_CONNECTOR_VERSION:-3.0.1}
DELTA_LAKE_VERSION=${DELTA_LAKE_VERSION:-1.0.0}
HADOOP_VERSION=${HADOOP_VERSION:-3.2.0}

# Execution
spark-submit --packages org.apache.hadoop:hadoop-aws:${HADOOP_VERSION},org.mongodb.spark:mongo-spark-connector_2.12:${MONGODB_CONNECTOR_VERSION},io.delta:delta-core_2.12:${DELTA_LAKE_VERSION} $@
