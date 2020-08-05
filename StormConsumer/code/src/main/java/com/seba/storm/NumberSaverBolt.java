package com.seba.storm;

import java.sql.Timestamp;

import com.datastax.driver.core.Row;
import com.datastax.driver.core.Statement;
import com.datastax.driver.core.querybuilder.QueryBuilder;

import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Tuple;

public class NumberSaverBolt extends CassandraBaseBolt {

    /**
     *
     */
    private static final long serialVersionUID = 1L;

    @Override
    public void execute(Tuple input, BasicOutputCollector collector) {
        Integer number = input.getIntegerByField("number");
        Row row;
        long count = 0L;

        try {
            Statement selectQuery = QueryBuilder.select("count").from("numbers")
                .where(QueryBuilder.eq("number", number));
            
            row = session.execute(selectQuery).one();
            System.out.println(number);
            System.out.println(row);
            
            if (row != null) {
                count = row.getLong("count");
            }
            count++;
            // define the insertion query
            Statement insertQuery = QueryBuilder.insertInto("numbers")
                .value("number", number)
                .value("count", count)
                .value("update_date", new Timestamp(System.currentTimeMillis()));
            session.execute(insertQuery);
        } catch(Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        // nothing to do because this is the last point
    }
}