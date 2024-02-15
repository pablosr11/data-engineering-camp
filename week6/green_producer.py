import random
import time

from confluent_kafka import Producer

RIDE_TYPE = "green"  # green or fhv
RIDES_FILEPATH = f"/Users/ps/Downloads/{RIDE_TYPE}_tripdata_2019-01.csv"
SLEEP_BOUNDS = (0.4, 2)
TOPIC = f"rides_{RIDE_TYPE}"

p = Producer({"bootstrap.servers": "localhost:9092"})


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print(
            "{} - Message delivered to {} [{}]".format(
                RIDE_TYPE, msg.topic(), msg.partition()
            )
        )


with open(RIDES_FILEPATH, encoding="utf-8") as f:
    for data in f:

        print(f"Producing message: {data}")

        # make it a bit slower to check the delivery report
        time.sleep(random.uniform(SLEEP_BOUNDS[0], SLEEP_BOUNDS[1]))

        # Trigger any available delivery report callbacks from previous produce() calls
        p.poll(0)

        # Asynchronously produce a message. The delivery report callback will
        # be triggered from the call to poll() above, or flush() below, when the
        # message has been successfully delivered or failed permanently.
        p.produce(TOPIC, data.encode("utf-8"), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
