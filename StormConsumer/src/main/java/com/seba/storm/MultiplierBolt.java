package com.seba.storm;

import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseBasicBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;
import org.json.JSONObject;

// this bolt take the number from kafka and multiplies it by 100
public class MultiplierBolt extends BaseBasicBolt {

    private static final long serialVersionUID = 1L;

    @Override
    public void execute(Tuple input, BasicOutputCollector collector) {
        // take json from kafka
        String json = input.getStringByField("value");
        JSONObject obj = new JSONObject(json);

        Integer number = obj.getBigInteger("number").intValue();
        collector.emit(new Values(number*100));
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("number"));
    }
    
}