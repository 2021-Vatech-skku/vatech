import com.fasterxml.jackson.databind._
import org.apache.kafka.clients.CommonClientConfigs
import org.apache.kafka.common.config.SaslConfigs
import org.apache.kafka.streams.scala.StreamsBuilder
import org.apache.kafka.streams.scala.ImplicitConversions._
import org.apache.kafka.streams.scala.kstream._
import org.apache.kafka.streams.{KafkaStreams, KeyValue, StreamsConfig}
import org.apache.kafka.streams.scala.serialization.Serdes._
import org.apache.kafka.common.serialization.{Deserializer, Serde, Serdes, Serializer}
//import com.fasterxml.jackson.module.scala.{DefaultScalaModule, ScalaObjectMapper}
//import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import io.circe.syntax.EncoderOps
//import org.apache.kafka.common.protocol.types.Field.Int32
//import org.apache.kafka.connect.json.{JsonDeserializer, JsonSerializer}
//import org.apache.kafka.streams.scala.Serdes.String
//import org.apache.kafka.streams.Topology
//import org.json4s._
//import org.json4s.jackson.JsonMethods._
//import org.json4s.native.Json
//import org.json4s.DefaultFormats
//import org.json4s.JString
//import org.json4s.Implicits

import org.mongodb.scala.bson.ObjectId

import java.util.Date
import java.util
import java.util.Properties
import java.time.Duration
import scala.collection.mutable.Map
import Serdes._

import io.circe._, io.circe.parser._
import cats.syntax.either._


object convertjson extends App {

  //  def jsonStrToMap(jsonStr: String): Map[String, Any] = {
  //    implicit val formats = org.json4s.DefaultFormats
  //
  //    parse(jsonStr).extract[Map[String, Any]]
  //  }

  case class patientInfo(
                          _id : ObjectId,
                          customerGroupID : Array[Any],
                          hospitalId : String,
                          id : String,
                          address : String,
                          birthDate : Date,
                          cellphoneNumber : String,
                          chartNumber : String,
                          consentTo3rdPartyAgreement : Boolean,
                          doctor : String,
                          email : String,
                          grade : String,
                          memo : String,
                          name : String,
                          newOrExistingPatient : String,
                          personalInformationAgreement : Boolean,
                          recommender : String,
                          sex : String,
                          staff : String,
                          telephoneNumber : String,
                          tendency : String,
                          visitingRoute : String,
                          finalVisitingDate : Date,
                          lastModifiedStaff : String,
                          createTime : Date,
                          lastModifiedTime : Int,
                          family : Array[Any],
                          recommenderInfo : Array[Any],
                          __v : Int,
                          findMemo : String,
                          identification : String,
                          paymentAmount : String,
                          etcPaymentAmount : String,
                          latestPlStatus : String



                        )

  val config: Properties = {
    val p = new Properties()
    //id for specify kafka streams app
    p.put(StreamsConfig.APPLICATION_ID_CONFIG, "scala-application5")
    val bootstrapServers = if (args.length > 0) args(0) else "kafka-kafka-bootstrap:9093"        //"172.26.50.121:31669"
    p.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers)
    //which data type to read and write
    p.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,Serdes.String().getClass)
    p.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,Serdes.String().getClass)
    p.put(StreamsConfig.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT")
    p.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT")
    p.put(SaslConfigs.SASL_MECHANISM,"SCRAM-SHA-512")
    p.put(SaslConfigs.SASL_JAAS_CONFIG, "org.apache.kafka.common.security.scram.ScramLoginModule required username=\"jee-user\"  password=\"kEbUG3h8HWRB\";")
    p
  }

  //val jns  = new JsonSerializer()
  //val jnd = new JsonDeserializer()
  //val jnserde = Serdes.serdeFrom(jns,jnd)
  //val valvalval = new

  //builder to define topology which consists of data stream
  val builder = new StreamsBuilder()

  //create the kstream from the topic
  // val inputdata: KStream[String, Map[String,String]] = builder.stream[String, Map[String,String]]("jee.clever.dev0-patient.10")//builder.stream("..")(Consumed.`with`(Serdes.String(),jnserde)) // .stream[String, JsonNode]("")       //"jee.patinets"
  val inputdata2: KStream[String,String] = builder.stream[String,String]("jee.clever.dev0-patient.10")//(Consumed.`with`(Serdes.String(),)        //(Consumed.`with`(Serdes.String(),jnserde))
  //  val om = new ObjectMapper() with ScalaObjectMapper
  //  om.registerModule(DefaultScalaModule)
  //    .registerModule(new JavaTimeModule)
  //  om.enable(DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT)
  //    .disable(DeserializationFeature.FAIL_ON_MISSING_CREATOR_PROPERTIES)
  //    .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)



  //modify the data from stream
  val filtered2: KStream[String,String] = inputdata2
    .mapValues(v =>{
      val temp : Json = parse(v).getOrElse(Json.Null)
      val cursor : HCursor = temp.hcursor
      val Cursor : ACursor = cursor.downField("\"name\"").withFocus(j=>j.mapString(s=>s.replace(s.substring(0,s.length),"***")))//.downField("name").withFocus(j=>j.mapString(value=>value.replace(value.substring(0,value.length),"***")))
      val result : Option[Json] = Cursor.top
      result.asJson.noSpaces //.toString
      //temp.asJson.noSpaces
    } )
  // val filtereddata2: KStream[String,String] = inputdata2.mapValues((k,v)=>jsonStrToMap(v)).mapValues(v2=>{v2("name")="****"; v2}).mapValues(v3=>Json(DefaultFormats).write(v3))//if(v2.contains("name")){v2("name")="*****";  v2})  //.to("jee.filterd.test")
  //  val filtereddata3: KStream[String,String] = inputdata2.mapValues(v=>jsonStrToMap(v))
  //    .mapValues(v2=>{v2("name")="****"; v2})
  //    .mapValues(v3=>Json(DefaultFormats).write(v3))//if(v2.contains("name")){v2("name")="*****";  v2})  //.to("jee.filterd.test")
  //val filtereddata4 : KStream[String,String] = inputdata2.mapValues(v=>{var map :Map[String,Any] = om.readValue(v,classOf[Map[String,Any]]); map}).mapValues(v1=>{v1("\"name\"")="*****"; om.writeValueAsString(v1)})
  //val filtereddata5 : KStream[String,patientInfo] = inputdata2.mapValues(v=> {parse(v).extract[patientInfo]})


  // Write the results to a new Kafka topic
  // inputdata2.to("jee.filtered.test")
  filtered2.to("jee.filtered.test3")//(Produced.`with`(Serdes.String(),Serdes.String()))

  // create topology
  val streams: KafkaStreams = new KafkaStreams(builder.build(), config)
  streams.start()

  // Add shutdown hook to respond to SIGTERM and gracefully close Kafka Streams
  sys.ShutdownHookThread {
    streams.close(Duration.ofSeconds(10))
  }
}

