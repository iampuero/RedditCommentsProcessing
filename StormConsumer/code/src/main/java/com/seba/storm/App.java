package com.seba.storm;

import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.kafka.spout.KafkaSpout;
import org.apache.storm.kafka.spout.KafkaSpoutConfig;
import org.apache.storm.topology.TopologyBuilder;

/**
 * Hello world!
 *
 */
public class App{

    public static void main( String[] args ){
        String kafka_host = "localhost:9092"; 
        // String kafka_host = System.getenv("STORM_KAFKA_CONNECT");
        String kafka_topic = "Reddit";
        // creation of the toppology
        TopologyBuilder builder = new TopologyBuilder();
        // in our case the spout is going to be a kafka consumer
        builder.setSpout("kafka_spout", new KafkaSpout<>(KafkaSpoutConfig.builder(kafka_host, kafka_topic).build()));
        // in this bolts we procese the data
        builder.setBolt("read_json_bolt", new ReadJsonBolt()).shuffleGrouping("kafka_spout");
        // in this bolt we count the data
        builder.setBolt("counter_bolt", new CounterBolt()).shuffleGrouping("read_json_bolt");
        // this bolt save the data in cassandra
        builder.setBolt("word_saver_bolt", new StringSaverBolt(), 1).shuffleGrouping("counter_bolt");

        // second version: in this case the bolt that save the data make a query to get the previus value
        // comment the version above and discomment this part to use it
        // TopologyBuilder builder = new TopologyBuilder();
        // // in our case the spout is going to be a kafka consumer
        // builder.setSpout("kafka_spout", new KafkaSpout<>(KafkaSpoutConfig.builder(kafka_host, kafka_topic).build()));
        // // in this bolts we procese the data
        // builder.setBolt("read_json_bolt", new ReadJsonBolt()).shuffleGrouping("kafka_spout");
        // // this bolt save the data in cassandra
        // builder.setBolt("word_saver_bolt", new StringUpdateBolt(), 1).shuffleGrouping("read_json_bolt");

        Config config = new Config();
        // config.put(Config.NIMBUS_THRIFT_PORT, 6627);
        // config.put(Config.STORM_ZOOKEEPER_PORT, 2181);
        // config.setDebug(true);
        
        try {
            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("HelloTopology", config, builder.createTopology());
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
