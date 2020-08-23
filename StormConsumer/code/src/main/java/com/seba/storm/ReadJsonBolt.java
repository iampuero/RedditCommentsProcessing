package com.seba.storm;

import java.util.Arrays;
import java.util.List;

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
    private static List<String> stopWords = Arrays.asList("a","about","above","after","again","against","all","am","an","and","any","are","arent","as",
    "at","be","because","been","before","being","below","between","both","but","by","cant","cannot",
    "could","couldnt","did","didnt","do","does","doesnt","doing","dont","down","during","each","few",
    "for","from","further","had","hadnt","has","hasnt","have","havent","having","he","hed","hell",
    "hes","her","here","heres","hers","herself","him","himself","his","how","hows","i","id","ill",
    "im","ive","if","in","into","is","isnt","it","its","its","itself","lets","me","more","most",
    "mustnt","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our",
    "ours	ourselves","out","over","own","same","shant","she","shed","shell","shes","should","shouldnt",
    "so","some","such","than","that","thats","the","their","theirs","them","themselves","then","there","theres",
    "these","they","theyd","theyll","theyre","theyve","this","those","through","to","too","under","until","up",
    "very","was","wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where",
    "wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt","you","youd","youll",
    "youre","youve","your","yours","yourself","yourselves","just","like","will","can");

    @Override
    public void execute(Tuple input, BasicOutputCollector collector) {
        // take json from kafka
        String json = input.getStringByField("value");
        JSONObject obj = new JSONObject(json);
        try {
            // extract the body and the subreddit where this is going to live
            String text = obj.getString("body").toLowerCase().replaceAll("[^a-z ]", "");
            String subreddit = obj.getString("subreddit");
            Integer ups = obj.getInt("ups");
            Integer downs = obj.getInt("downs");
            // extract the words from the text
            String[] words = text.split("\\s+");
            for (String string : words) {
                // send the word to the cassandra bolt
                if(!stopWords.contains(string))
                    collector.emit(new Values(string, subreddit, ups + downs));
            }   
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("word", "subreddit", "score"));
    }
}