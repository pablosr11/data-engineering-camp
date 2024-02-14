Kafka

1. Format logs directories
   `bin/kafka-storage.sh format -t "$(bin/kafka-storage.sh random-uuid)" -c config/kraft/server.properties`

2. Start the server
   `bin/kafka-server-start.sh config/kraft/server.properties`

3. Create topic
   `bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092`

4. Create producer
   `bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092`

5. Create consumer
   `bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092`

6. List topics
   `bin/kafka-topics.sh --list --bootstrap-server localhost:9092`

7. Describe topic
   `bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server localhost:9092`

8. Kafka Connect w/ files (defaults to local test.txt and test.sink.txt for in/out). Requires manually adding the connect jar to plugin.path
   `bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties`


## Week 6 Homework
1. Create topics for rides_fhv, rides_green and rides_all:
   `bin/kafka-topics.sh --create --topic rides_fhv --bootstrap-server localhost:9092`
   `bin/kafka-topics.sh --create --topic rides_green --bootstrap-server localhost:9092`
   `bin/kafka-topics.sh --create --topic rides_all --bootstrap-server localhost:9092`
2. ✅ Producer that reads csv files and publish rides in corresponding kafka topics (such as rides_green, rides_fhv)

3. ✅ Pyspark-streaming-application that reads two kafka topics

4. Pyspark streaming-app that consumes both of them in topic rides_all and apply aggregations to find most popular pickup location.
