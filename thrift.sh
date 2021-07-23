#!/bin/bash

# Packages Versions
DELTA_LAKE_VERSION=${DELTA_LAKE_VERSION:-1.0.0}
HADOOP_VERISON=${HADOOP_VERISON:-3.2.0}

# Execution
cd $SPARK_HOME
$SPARK_HOME/sbin/start-thriftserver.sh --conf spark.sql.warehouse.dir=$SPARK_HOME \
  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
  --conf spark.hadoop.fs.s3a.access.key=haruband \
  --conf spark.hadoop.fs.s3a.secret.key=haru1004 \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
  --conf spark.hadoop.fs.s3a.endpoint=https://minio.develop.vsmart00.com \
  --packages io.delta:delta-core_2.12:${DELTA_LAKE_VERSION},org.apache.hadoop:hadoop-aws:${HADOOP_VERISON} $@

# create table patients using DELTA location "s3a://bigdata/patients"