FROM ubuntu:21.04
USER root:root
RUN mkdir -p /scalaws
COPY . /scalaws
RUN cd /scalaws
RUN apt-get update
RUN apt-get install -y scala
RUN apt-get install -y curl
RUN apt-get install -y gnupg2
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee /etc/apt/sources.list.d/sbt_old.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add
RUN apt-get update
RUN apt-get install -y sbt
CMD ["./autoSBT.sh"]

