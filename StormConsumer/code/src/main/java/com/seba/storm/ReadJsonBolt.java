package com.seba.storm;

import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseBasicBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;
import org.json.JSONObject;

public class ReadJsonBolt extends BaseBasicBolt {

    /**
     *
     */
    private static final long serialVersionUID = 1L;

    @Override
    public void execute(Tuple input, BasicOutputCollector collector) {
        // take json from kafka
        String json = input.getStringByField("value");
        JSONObject obj = new JSONObject(json);
        // extract the body and the subreddit where this is going to live
        String text = obj.getString("body");
        String subreddit = obj.getString("subreddit");
        // extract the words from the text
        String[] words = text.split("\\s+");
        for (String string : words) {
            // send the word to the cassandra bolt
            collector.emit(new Values(string, subreddit));
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("word", "subreddit"));
    }
}