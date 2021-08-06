FROM quay.io/strimzi/kafka:0.22.1-kafka-2.7.0
USER root:root
RUN mkdir -p /opt/kafka/plugins/
COPY ./libs/mongodb-kafka-connect-mongodb-1.5.1/lib/ /opt/kafka/plugins/mongodb-kafka-connect-mongdb-1.5.1
COPY ./libs/confluentinc-kafka-connect-s3-10.0.1/ /opt.kafka/plugins/confluentinc-kafka-connect-s3-10.0.1
USER 1001

