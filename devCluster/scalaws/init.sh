set scalaVersion := "2.13.6"
set libraryDependencies += "org.apache.kafka" %% "kafka" % "2.8.0"
set libraryDependencies += "org.apache.kafka" % "kafka-streams" % "2.8.0"
set libraryDependencies += "org.apache.kafka" %% "kafka-streams-scala" % "2.8.0"
set libraryDependencies += "org.apache.kafka" % "kafka-clients" % "2.8.0"
set libraryDependencies += "org.slf4j" % "slf4j-simple" % "1.8.0-alpha2"

set initialCommands :=""
set initialCommands += "import org.apache.kafka.streams.scala.StreamsBuilder, org.apache.kafka.streams.scala._, org.apache.kafka.streams._, org.apache.kafka.common.serialization.Serdes, java.util.Properties, java.time.Duration"
session save
compile


