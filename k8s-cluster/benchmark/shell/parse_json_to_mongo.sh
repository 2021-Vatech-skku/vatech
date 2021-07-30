#!/bin/sh
FILENAME=$1
BASENAME=${FILENAME%.*}
BASENAME=${BASENAME#./}

echo "parsing $1.."
METRICNAME=(
    "checks" 
    "data_received" 
    "data_sent" 
    "group_duration" 
    "http_req_blocked" 
    "http_req_connecting" 
    "http_req_duration" 
    "http_req_failed" 
    "http_req_receiving" 
    "http_req_sending" 
    "http_req_tls_handshaking" 
    "http_req_waiting" 
    "http_reqs" 
    "iteration_duration" 
    "iterations" 
    "vus" 
    "vus_max" 
)

for METRIC in ${METRICNAME[@]}
do
    METRIC=`sed -e 's/^"//' -e 's/"$//' <<< $METRIC`
    echo "import ${METRIC} collection to mongodb.."
    jq --arg METRIC $METRIC '. | select(.type=="Point") | select(.metric==$METRIC)' $FILENAME | 
    mongoimport mongodb://mongo.it.vsmart00.com \
        --db "benchmark" \
        --collection "${BASENAME}_${METRIC}" \
        -u haruband -p haru1004 \
        --authenticationDatabase=admin \
        --mode=insert -j 8 \
        --type=json --drop \
        --verbose
done
