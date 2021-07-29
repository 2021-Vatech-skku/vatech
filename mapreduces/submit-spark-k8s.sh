#!/bin/bash

PYTHON_SOURCE=${1:-pisimple.py} && shift

SPARK_IMAGE=${SPARK_IMAGE:-cleverpms/myspark}
SPARK_EXECUTORS=${SPARK_EXECUTORS:-3}
SPARK_MEMORY=${SPARK_MEMORY:-1024m}
K8S_MASTER=${K8S_MASTER:-$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')}

BASENAME=$(basename -- ${PYTHON_SOURCE})
FILENAME="${BASENAME%.*}"

spark-submit --master k8s://${K8S_MASTER} \
    --deploy-mode cluster \
    --name ${FILENAME} \
    --conf spark.executor.instances=${SPARK_EXECUTORS} \
    --executor-memory ${SPARK_MEMORY} \
    --conf spark.kubernetes.namespace=spark \
    --conf spark.kubernetes.driver.label.spark-app=${FILENAME} \
    --conf spark.kubernetes.container.image=${SPARK_IMAGE} \
    --conf spark.kubernetes.container.image.pullPolicy=Always \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    local:///opt/spark/work-dir/${PYTHON_SOURCE} $@
