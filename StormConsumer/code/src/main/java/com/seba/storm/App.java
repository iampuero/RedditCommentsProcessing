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
        
        TopologyBuilder builder = new TopologyBuilder();
        // sample is the topic and values are json like {'number': 0}
        builder.setSpout("kafka_spout", new KafkaSpout<>(KafkaSpoutConfig.builder("localhost:9093", "numbers").build()), 1);
        // builder.setSpout("IntegerSpout", new IntergerSpout());
        builder.setBolt("multiplier_bolt", new MultiplierBolt()).shuffleGrouping("kafka_spout");
        builder.setBolt("number_saver_bolt", new NumberSaverBolt(), 1).shuffleGrouping("multiplier_bolt");

        Config config = new Config();
        config.put(Config.NIMBUS_THRIFT_PORT, 6627);
        config.put(Config.STORM_ZOOKEEPER_PORT, 2181);
        // config.setDebug(true);
        
        LocalCluster cluster = null;

        try {
            cluster = new LocalCluster();
            cluster.submitTopology("HelloTopology", config, builder.createTopology());
            Thread.sleep(10000);
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
