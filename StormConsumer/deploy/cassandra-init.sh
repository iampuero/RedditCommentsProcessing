# https://github.com/docker-library/cassandra/issues/104#issuecomment-413193337
CQL="
CREATE KEYSPACE IF NOT EXISTS reddit WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true;
CREATE TABLE IF NOT EXISTS reddit.word_counter (subreddit text, word text, count bigint, score bigint,PRIMARY KEY(subreddit, word));"

until echo $CQL | cqlsh; do
  echo "cqlsh: Cassandra is unavailable to initialize - will retry later"
  sleep 2
done &

exec /docker-entrypoint.sh "$@"