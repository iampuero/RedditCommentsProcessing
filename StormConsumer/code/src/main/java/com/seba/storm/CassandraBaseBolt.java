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
        cluster = Cluster.builder().addContactPoint("localhost").build();
        session = cluster.connect("test_numbers");
    }

    @Override
    public void cleanup(){
        session.close();
        cluster.close();
    }
}