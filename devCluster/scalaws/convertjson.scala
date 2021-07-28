import com.fasterxml.jackson.databind
import org.apache.kafka.clients.CommonClientConfigs
import org.apache.kafka.common.config.SaslConfigs
import org.apache.kafka.streams.scala.StreamsBuilder
import org.apache.kafka.streams.scala.kstream._
import org.apache.kafka.streams.{KafkaStreams, KeyValue, StreamsConfig}
import org.apache.kafka.streams.scala.serialization.Serdes._
import org.apache.kafka.streams.scala.ImplicitConversions._
import org.apache.kafka.common.serialization.{Deserializer, Serde, Serdes, Serializer}
import com.fasterxml.jackson.databind.JsonNode
import com.fasterxml.jackson.databind.node.ObjectNode
import com.fasterxml.jackson.databind.node.JsonNodeFactory
import com.fasterxml.jackson.databind.node.ObjectNode
import org.apache.kafka.connect.json.{JsonDeserializer, JsonSerializer}
import org.apache.kafka.streams.scala.Serdes.String
import org.apache.kafka.streams.Topology
import org.json4s._
import org.json4s.jackson.JsonMethods._



import java.util.Properties
import java.time.Duration
//import scala.collection.mutable.Map
import Serdes._


object convertjson extends App {

  val config: Properties = {
    val p = new Properties()
    //카프카 스트림즈 애플리케이션을 구분할 아이디
    p.put(StreamsConfig.APPLICATION_ID_CONFIG, "scala-application")
    val bootstrapServers = if (args.length > 0) args(0) else "kafka-kafka-bootstrap:9093"        //"172.26.50.121:31669"
    p.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers)
    //데이터를 어떠한 형식으로 Read/Write할지를 설정(키/값의 데이터 타입을 지정) - 문자열
    p.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,Serdes.String().getClass)
    p.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,Serdes.String().getClass)
    p.put(StreamsConfig.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT")
    p.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT")
    p.put(SaslConfigs.SASL_MECHANISM,"SCRAM-SHA-512")
    p.put(SaslConfigs.SASL_JAAS_CONFIG, "org.apache.kafka.common.security.scram.ScramLoginModule required username=\"jee-user\"  password=\"kEbUG3h8HWRB\";")
    p
  }

  val jns  = new JsonSerializer()
  val jnd = new JsonDeserializer()
  val jnserde = Serdes.serdeFrom(jns,jnd)
  //val valvalval = new

  //builder to define topology which consists of data stream
  val builder = new StreamsBuilder()

  //create the kstream from the topic
  // val inputdata: KStream[String, Map[String,String]] = builder.stream[String, Map[String,String]]("jee.clever.dev0-patient.10")//builder.stream("..")(Consumed.`with`(Serdes.String(),jnserde)) // .stream[String, JsonNode]("")       //"jee.patinets"
  val inputdata2: KStream[String,JsonNode] = builder.stream[String,JsonNode]("")(Consumed.`with`(Serdes.String(),jnserde))

  //modify the data from stream
  //val filtered1: KStream[String,Map[String,String]] //= inputdata.mapValues(value => value.filter(k=>k._2.equals("\"name\"")).map{case(k1,v1)=>(k1,v1.replace(v1.substring(0,v1.length),"\"***\""))})   //replace(v1.substring(0,v1.length),"***")))
  // inputdata.filter((key,value)=>key.equals("\"name\"")).mapValues((key, value)=>value.replace(value.substring(0,value.length),"***")) //filter((key,value)=>key.equals("foo")).
  // val filtered2: KStream[String,String] = inputdata.filterNot((key,value)=>key.equals("\"name\""))
  //val filtereddata2: KStream[String,JsonNode] =


  // Write the results to a new Kafka topic
  // filtered1.to("jee.filtered.test")
  //  filtered2.to("jee.filtered.test")

  // create topology
  val streams: KafkaStreams = new KafkaStreams(builder.build(), config)
  streams.start()
  println(inputdata2.getClass)

  // Add shutdown hook to respond to SIGTERM and gracefully close Kafka Streams
  sys.ShutdownHookThread {
    streams.close(Duration.ofSeconds(10))
  }
}



//userClicksStream
//
//   // Join the stream against the table.
//   .leftJoin(userRegionsTable)((clicks, region) => (if (region == null) "UNKNOWN" else region, clicks.clicks))