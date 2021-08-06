import org.apache.kafka.clients.CommonClientConfigs
import org.apache.kafka.common.config.SaslConfigs
import org.apache.kafka.streams.scala.StreamsBuilder
import org.apache.kafka.streams.scala.ImplicitConversions._
import org.apache.kafka.streams.scala.kstream._
import org.apache.kafka.streams.{KafkaStreams, KeyValue, StreamsConfig}
import org.apache.kafka.streams.scala.serialization.Serdes._
import org.apache.kafka.common.serialization.{Deserializer, Serde, Serdes, Serializer}
import org.json4s.jackson.JsonMethods
import org.json4s.jackson.Serialization
import org.json4s._
import scala.collection.mutable.Map
import java.util.Properties
import java.time.Duration
import scala.collection.mutable
import org.apache.kafka.clients.consumer.ConsumerConfig

object convertjson extends App {
  val config: Properties = {
    val p = new Properties()
    p.put(StreamsConfig.APPLICATION_ID_CONFIG, "scala-application12")
    val bootstrapServers = if (args.length > 0) args(0) else "kafka-kafka-bootstrap:9093"
    p.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers)
    //p.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, 1000*60*60*24)

    //which data type to read and write
    p.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,Serdes.String().getClass)
    p.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,Serdes.String().getClass)
    p.put(StreamsConfig.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT")
    p.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT")
    p.put(SaslConfigs.SASL_MECHANISM,"SCRAM-SHA-512")
    p.put(SaslConfigs.SASL_JAAS_CONFIG, "org.apache.kafka.common.security.scram.ScramLoginModule required username=\"jee-user\"  password=\"kEbUG3h8HWRB\";")
    p
  }

  //builder to define topology which consists of data stream
  val builder = new StreamsBuilder()

  //create the kstream from the topic
  val inputdata2: KStream[String,String] = builder.stream[String,String]("jee.clever.dev0-patient.test")

  //modify the data from stream
  val filtered2: KStream[String,String] = inputdata2
    .mapValues(v =>{
      implicit val formats = DefaultFormats
      val mappedVal : mutable.Map[String,Map[String,Any]] = JsonMethods.parse(v).extract[mutable.Map[String,Map[String,Any]]]
      val mappedFullDoc : mutable.Map[String,Any] =JsonMethods.parse(mappedVal("payload")("fullDocument").toString).extract[mutable.Map[String,Any]]
      mappedFullDoc("name") = "*****"
      mappedVal("payload")("fullDocument") = Serialization.write(mappedFullDoc)
      Serialization.write(mappedVal)
    } )

  filtered2.to("jee.clever.dev0-patient.filtered.test")

  // create topology
  val streams: KafkaStreams = new KafkaStreams(builder.build(), config)
  streams.start()

  // Add shutdown hook to respond to SIGTERM and gracefully close Kafka Streams
  sys.ShutdownHookThread {
    streams.close(Duration.ofSeconds(10))
  }
}

