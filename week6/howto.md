Kafka

1. Format logs directories
   `bin/kafka-storage.sh format -t "$(bin/kafka-storage.sh random-uuid)" -c config/kraft/server.properties`

2. Start the server
   `bin/kafka-server-start.sh config/kraft/server.properties`

3. Create topic
   `bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092`

