#!/bin/bash

# Packages Versions
DELTA_LAKE_VERSION=${DELTA_LAKE_VERSION:-1.0.0}

# Execution
cd $SPARK_HOME
$SPARK_HOME/sbin/start-thriftserver.sh --conf spark.sql.warehouse.dir=$SPARK_HOME --packages io.delta:delta-core_2.12:${DELTA_LAKE_VERSION} $@
