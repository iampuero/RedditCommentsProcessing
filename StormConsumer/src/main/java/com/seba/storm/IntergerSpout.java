package com.seba.storm;

import java.util.Map;
import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;

// this is a example class
public class IntergerSpout extends BaseRichSpout{
    /**
     *
     */
    private static final long serialVersionUID = 1L;
    SpoutOutputCollector spoutOutputCollector;
    private Integer index = 0;

    public void open(Map<String, Object> map, TopologyContext topologyContext, SpoutOutputCollector spoutOutputCollector){
        this.spoutOutputCollector = spoutOutputCollector;
    }

    public void nextTuple(){
        if (index < 100) {
            this.spoutOutputCollector.emit(new Values(index*1000));
            index++;
        }
    }

    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer){
        outputFieldsDeclarer.declare(new Fields("fields"));
    }
}