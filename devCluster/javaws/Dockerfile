FROM ubuntu:latest
USER root:root
RUN mkdir -p /javaws
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk
#RUN apt-get install -y mvn
RUN apt-get install -y maven
COPY . /javaws
RUN cd /javaws
#RUN apt-get install -y curl
#RUN apt-get install -y gnupg2

