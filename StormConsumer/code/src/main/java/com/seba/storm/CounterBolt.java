package com.seba.storm;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseBasicBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

public class CounterBolt implements IRichBolt {
  /**
   *
   */
  private static final long serialVersionUID = 1L;
  HashMap<String, HashMap<String, Integer[]>> counterMap;
  private OutputCollector collector;

  @Override
  public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
    this.counterMap = new HashMap<String, HashMap<String, Integer[]>>();
    this.collector = collector;
  }

  @Override
  public void execute(Tuple input) {
    String word = input.getStringByField("word");
    String subreddit = input.getStringByField("subreddit");
    Integer score = input.getIntegerByField("score");

    if(!counterMap.containsKey(subreddit)){
      counterMap.put(subreddit, new HashMap<String, Integer[]>());
    } if(!counterMap.get(subreddit).containsKey(word)){
      Integer[] counterArray = new Integer[2];
      counterArray[0] = 0;
      counterArray[1] = 0;
      counterMap.get(subreddit).put(word, counterArray);
    } else{
      Integer[] counters = counterMap.get(subreddit).get(word);
      counters[0] ++;
      counters[1] = counters[1] + score;
      counterMap.get(subreddit).put(word, counters);
    }

    Integer[] temp_values = counterMap.get(subreddit).get(word);

    if (temp_values[0] == 10) {
      collector.emit(new Values(word, subreddit, temp_values[0], temp_values[1]));
      // reset the counter
      Integer[] counterArray = new Integer[2];
      counterArray[0] = 0;
      counterArray[1] = 0;
      counterMap.get(subreddit).put(word, counterArray);
    }
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("word", "subreddit", "counter", "score"));
  }

  @Override
  public void cleanup() {
    for(Map.Entry<String, HashMap<String, Integer[]>> subrredit : counterMap.entrySet()){
      System.out.println("Subrreddit: " + subrredit.getKey());
      for(Map.Entry<String, Integer[]> words : subrredit.getValue().entrySet())
        System.out.println("Word: " + words.getKey() + ", values: " + words.getValue()[0] + " " + words.getValue()[1]);
    }
  }
    
  @Override
  public Map<String, Object> getComponentConfiguration() {
    return null;
  }
    
}