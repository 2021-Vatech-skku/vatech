initialCommands:="import org.apache.kafka.streams.scala.StreamsBuilder, org.apache.kafka.streams.scala.kstream._, org.apache.kafka.streams.{KafkaStreams, KeyValue,StreamsConfig}, org.apache.kafka.streams.scala.serialization.Serdes._, org.apache.kafka.streams.scala.ImplicitConversions._, org.apache.kafka.common.serialization.Serdes, java.util.Properties, java.time.Duration"



name := "kafkastream"

scalaVersion := "2.13.6"

libraryDependencies += "org.apache.kafka" %% "kafka" % "2.8.0"

libraryDependencies += "org.apache.kafka" % "kafka-streams" % "2.8.0"

libraryDependencies += "org.apache.kafka" %% "kafka-streams-scala" % "2.8.0"

libraryDependencies += "org.apache.kafka" % "kafka-clients" % "2.8.0"

libraryDependencies += "org.slf4j" % "slf4j-simple" % "1.8.0-alpha2"

libraryDependencies += "org.apache.kafka" %% "kafka" % "2.8.0"

libraryDependencies += "org.apache.kafka" % "kafka-streams" % "2.8.0"

libraryDependencies += "org.apache.kafka" %% "kafka-streams-scala" % "2.8.0"

libraryDependencies += "org.apache.kafka" % "kafka-clients" % "2.8.0"

libraryDependencies += "org.slf4j" % "slf4j-simple" % "1.8.0-alpha2"

