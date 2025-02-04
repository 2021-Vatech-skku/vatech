name := "kafkastream"

version := "0.1"

scalaVersion := "2.13.6"


libraryDependencies += "org.apache.kafka" %% "kafka" % "2.8.0"
libraryDependencies += "org.apache.kafka" % "kafka-streams" % "2.8.0"

libraryDependencies += "org.apache.kafka" %% "kafka-streams-scala" % "2.8.0"
//excludeDependencies += ExclusionRule("javax.ws.rs", "javax.ws.rs-api")
//libraryDependencies += "javax.ws.rs" % "javax.ws.rs-api" % "2.1.1"
//libraryDependencies += "org.mongodb.kafka" % "mongo-kafka-connect" % "1.6.0"

//libraryDependencies += "commons-io" % "commons-io" % "2.11.0"
libraryDependencies += "org.apache.kafka" % "kafka-clients" % "2.8.0"
libraryDependencies += "org.slf4j" % "slf4j-simple" % "1.8.0-alpha2"



