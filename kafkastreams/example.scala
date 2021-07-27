

import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.kafka.streams.kstream.ValueTransformer
import org.slf4j.Logger
import org.apache.kafka.streams.scala.StreamsBuilder
import org.apache.kafka.common.IsolationLevel
import org.apache.kafka.common.serialization.Serializer

import java.time.Duration
import org.apache.kafka.streams.scala.kstream._
import org.apache.kafka.streams.{KafkaStreams, KeyValue, StreamsConfig}
import org.apache.kafka.streams.scala.serialization.Serdes._
import org.apache.kafka.streams.scala.ImplicitConversions._
//import org.apache.kafka.streams.scala.serialization.Serdes
import org.apache.kafka.common.serialization.Serdes

import java.util.Properties
import java.util.concurrent.CountDownLatch


object example extends App {



  val config: Properties = {
    val p = new Properties()
    //카프카 스트림즈 애플리케이션을 유일할게 구분할 아이디
    p.put(StreamsConfig.APPLICATION_ID_CONFIG, "scala-application")
    val bootstrapServers = if (args.length > 0) args(0) else "localhost:9095"        //"172.26.50.121:31669"
    p.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers)
    //데이터를 어떠한 형식으로 Read/Write할지를 설정(키/값의 데이터 타입을 지정) - 문자열
    p.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,Serdes.String().getClass)
    p.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,Serdes.String().getClass)

    p
  }

//  val builder = new StreamsBuilder
//  val textLines: KStream[Array[Byte], String] = builder.stream[Array[Byte], String]("TextLineTopic")
//
//  // Variant 1: using `mapValues`
//  //val uppercasedWithMapValues: KStream[Array[Byte], String] = textLines.mapValues(_.toUpperCase())
//  //uppercasedWithMapValues.to("UppercasedTextLinesTopic")
//
//  // Variant 2: using `map`, modify both key and value
//  val originalAndUppercased: KStream[String, String] = textLines.map((_, value) => (value, value.toUpperCase()))
//
//  // Write the results to a new Kafka topic "OriginalAndUppercasedTopic".
//  originalAndUppercased.to("OriginalAndUppercasedTopic")
//
//  val streams: KafkaStreams = new KafkaStreams(builder.build(), config)
//  streams.start()
//
//  sys.ShutdownHookThread {
//    streams.close(Duration.ofSeconds(10))
//  }

  //val alp :Array[String] = Array("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z")

  val builder = new StreamsBuilder()

  val inputdata: KStream[String, String] = builder.stream[String, String]("lone-p1r1-2")       //"jee.patinets"
  println(inputdata)
  // Variant 1: using `mapValues`
  //val uppercasedWithMapValues: KStream[Array[Byte], String] = textLines.mapValues(_.toUpperCase())
  //uppercasedWithMapValues.to("UppercasedTextLinesTopic")
  // val transformer = new ValueTransformer[] {}
  // Variant 2: using `map`, modify both key and value

  val filtered1: KStream[String,String] =inputdata.filter((key,value)=>key.equals("\"address\"")).mapValues((key, value)=>value.replace("\"ki\"","***")) //filter((key,value)=>key.equals("foo")).
  val filtered2: KStream[String,String] = inputdata.filterNot((key,value)=>key.equals("\"address\""))

  //val filteredData1: KStream[String, String] = inputdata.filter((key,value)=>key=="address") //.map((key, value) => (key, value.toLowerCase().replaceAll(String, "*")))
  //val filteredData2: KStream[String,String] = filteredData1.filter((key,value) => key!="name")


  //val filteredData: KStream[String, String] = inputdata.map((key, value) => (key, value.toLowerCase().replaceAll(String,"*")))

  // Write the results to a new Kafka topic
  filtered1.to("lone-p1r1-output") //.to("lone-p1r1-result")
  filtered2.to("lone-p1r1-output")

  val streams: KafkaStreams = new KafkaStreams(builder.build(), config)
  streams.start()



  // Add shutdown hook to respond to SIGTERM and gracefully close Kafka Streams
  sys.ShutdownHookThread {
    streams.close(Duration.ofSeconds(10))
  }
}