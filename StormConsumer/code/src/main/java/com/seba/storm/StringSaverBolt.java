package com.seba.storm;

import java.sql.Timestamp;

import com.datastax.driver.core.Row;
import com.datastax.driver.core.Statement;
import com.datastax.driver.core.querybuilder.QueryBuilder;

import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Tuple;

public class StringSaverBolt extends CassandraBaseBolt {

    /**
     *
     */
    private static final long serialVersionUID = 1L;
    private String TABLE_NAME = "word_counter";

    @Override
    public void execute(Tuple input, BasicOutputCollector collector) {
        
        String word = input.getStringByField("word");
        String subreddit = input.getStringByField("subreddit");
        long score = input.getIntegerByField("score");
        long count = input.getIntegerByField("counter");

        try {
            // define the insertion query
            Statement insertQuery = QueryBuilder.insertInto(TABLE_NAME)
                .value("subreddit", subreddit)
                .value("word", word)
                .value("count", count)
                .value("score", score);
            session.execute(insertQuery);
        } catch(Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        // TODO Auto-generated method stub

    }
    
}