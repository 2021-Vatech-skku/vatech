name :="kafkaStreams"

scalaVersion :="2.13.6"

libraryDependencies += "org.apache.kafka" %% "kafka" % "2.8.0"

libraryDependencies += "org.apache.kafka" % "kafka-streams" % "2.8.0"

libraryDependencies += "org.apache.kafka" %% "kafka-streams-scala" % "2.8.0"

libraryDependencies += "org.apache.kafka" % "kafka-clients" % "2.8.0"

libraryDependencies += "org.slf4j" % "slf4j-simple" % "1.8.0-alpha2"

libraryDependencies += "org.json4s" % "json4s-jackson_2.13" % "4.0.3"

libraryDependencies += "org.json4s" % "json4s-native_2.13" % "4.0.3"

libraryDependencies += "com.fasterxml.jackson.module" %% "jackson-module-scala" % "2.12.2"

libraryDependencies += "com.fasterxml.jackson.datatype" % "jackson-datatype-jsr310" % "2.11.2"

libraryDependencies += "org.mongodb.scala" %% "mongo-scala-driver" % "2.9.0"

libraryDependencies += "io.circe" %% "circe-parser" % "0.14.1"

