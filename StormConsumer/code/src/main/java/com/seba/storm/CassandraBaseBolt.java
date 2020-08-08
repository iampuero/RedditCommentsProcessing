package com.seba.storm;

import java.util.Map;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Session;

import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.base.BaseBasicBolt;

public abstract class CassandraBaseBolt extends BaseBasicBolt{
    
    private static final long serialVersionUID = 1L;
    private Cluster cluster;
    protected Session session;

    @Override
    public void prepare(Map<String, Object> topoConf, TopologyContext context) {
        // String cassandra_host = System.getenv("STORM_CASSANDRA_CONNECT");
        String cassandra_host = "localhost";
        String cassandra_keyspace = "test_numbers";
        cluster = Cluster.builder().addContactPoint(cassandra_host).build();
        session = cluster.connect(cassandra_keyspace);
    }

    @Override
    public void cleanup(){
        session.close();
        cluster.close();
    }
}