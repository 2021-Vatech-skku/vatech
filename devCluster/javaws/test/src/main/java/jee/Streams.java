import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationConfig;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;

import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.apache.kafka.connect.json.JsonDeserializer;
import org.apache.kafka.connect.json.JsonSerializer;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.common.serialization.Deserializer;

import org.apache.log4j.BasicConfigurator;
import org.json.JSONObject;
import org.json.JSONException;

import com.fasterxml.jackson.databind.ObjectMapper;

import javax.lang.model.type.PrimitiveType;
import javax.security.sasl.SaslClient;
import java.util.Locale;
import java.util.Properties;
import java.io.IOException;

import org.json.simple.JSONArray;
//import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;



import java.util.HashMap;
import java.util.Map;



public class Streams {

    public static void main(final String[] args) {

        final String bootstrapServers = args.length > 0 ? args[0] : "kafka-kafka-bootstrap:9093";
        //final String bootstrapServers = args.length > 0 ? args[0] : "localhost:9095";
        System.out.println("check1");
        BasicConfigurator.configure();

        Deserializer<JsonNode> jsonDeserializer = new JsonDeserializer();
        Serializer<JsonNode> jsonSerializer = new JsonSerializer();
        Serde<JsonNode> jsonSerde = Serdes.serdeFrom(jsonSerializer, jsonDeserializer);




        final Properties streamsConfiguration = new Properties();
        // Give the Streams application a unique name.  The name must be unique in the Kafka cluster
        // against which the application is run.
        streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "data-masking-jee");
        streamsConfiguration.put(StreamsConfig.CLIENT_ID_CONFIG, "data-masking-client-jee");
        // Where to find Kafka broker(s).
        streamsConfiguration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        // Specify default (de)serializers for record keys and for record values.
        //streamsConfiguration.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.);
        //streamsConfiguration.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        streamsConfiguration.put(StreamsConfig.SECURITY_PROTOCOL_CONFIG, "SASL_PLAINTEXT");
        streamsConfiguration.put(SaslConfigs.SASL_MECHANISM, "SCRAM-SHA-512");
        streamsConfiguration.put(SaslConfigs.SASL_JAAS_CONFIG,"org.apache.kafka.common.security.scram.ScramLoginModule required username=\"jee-user\"  password=\"kEbUG3h8HWRB\";");


        final Serde<String> stringSerde = Serdes.String();

        // In the subsequent lines we define the processing topology of the Streams application.
        final StreamsBuilder builder = new StreamsBuilder();

        // Read the input Kafka topic into a KStream instance.
        final KStream<JsonNode, JsonNode> inputstr = builder.stream("jee.clever.dev0-patient.test",Consumed.with(jsonSerde,jsonSerde));

        //ObjectMapper mapper = new ObjectMapper();
        //mapper.enable(DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT);

        //2. Parser
        //JSONParser jp = new JSONParser();

        final KStream<JsonNode,JsonNode> filterstr = inputstr.mapValues(v->{
              //Object obj = jp.parse(v);

            //4. To JsonObject
            //JSONObject jsonOb = null;//(value->{
//            try {
//                jsonOb = (JSONObject)jp.parse(v);
//            } catch (ParseException e) {
//                e.printStackTrace();
//            }
            ((ObjectNode)v).put("name", "*****");
            System.out.println("check2");
            return (JsonNode) v;
        });

        System.out.println("check2");


        // Write (i.e. persist) the results to a new Kafka topic called "UppercasedTextLinesTopic".
        //
        // In this case we can rely on the default serializers for keys and values because their data
        // types did not change, i.e. we only need to provide the name of the output topic.
        filterstr.to("jee.filtered.test5");



        final KafkaStreams streams = new KafkaStreams(builder.build(), streamsConfiguration);
        // Always (and unconditionally) clean local state prior to starting the processing topology.
        streams.cleanUp();
        streams.start();

        // Add shutdown hook to respond to SIGTERM and gracefully close Kafka Streams
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));









    }








}
