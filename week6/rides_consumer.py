import os

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import SparkSession
from schemas import ALL_RIDE_SCHEMA, dispatch_schema, ride_schema

os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 pyspark-shell"
)


spark = SparkSession.builder.appName("RidesConsumer").getOrCreate()

TOPICS = ["quickstart-events", "rides_green", "rides_fhv"]
AGGREGATION_TIME = "10 seconds"

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", ",".join(TOPICS))
    .option("startingOffsets", "latest")
    .option("failOnDataLoss", "false")
    .load()
)


df = df.selectExpr("CAST(value AS STRING)")
split_col = F.split(df["value"], ",")
split_col_length = F.size(split_col)


# keep track of split_col length
df = df.withColumn("col_length", F.size(split_col))

if_20 = (
    split_col.getItem(5).cast(T.IntegerType()),
    split_col.getItem(6).cast(T.IntegerType()),
)
if_7 = (
    split_col.getItem(3).cast(T.IntegerType()),
    split_col.getItem(4).cast(T.IntegerType()),
)

df = df.withColumn(
    "PULocationID",
    F.when(split_col_length == 20, if_20[0]).when(split_col_length == 7, if_7[0]),
)

df = df.withColumn(
    "DOLocationID",
    F.when(split_col_length == 20, if_20[1]).when(split_col_length == 7, if_7[1]),
)


df = df.na.drop()
df.printSchema()

df = df.select("PULocationID", "DOLocationID").filter("PULocationID is not null")

# add timestamp
df = df.withColumn("timestamp", F.current_timestamp())

# add watermark so we can aggregate over time
df = df.withWatermark("timestamp", "10 minutes")


df_trip_count_by_pulocation = (
    df.groupBy(["PUlocationID"])
    .count()
    .withColumnRenamed("count", "value")
    .withColumnRenamed("PUlocationID", "key")
)


df_pu_location_count = (
    df_trip_count_by_pulocation.sort(F.col("value").desc())
    .limit(10)
    .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
)

(
    # both key and value as types.StringType
    df_pu_location_count.writeStream.outputMode("complete")
    .trigger(processingTime=AGGREGATION_TIME)
    .format("console")
    .start()
)

(
    df_pu_location_count.selectExpr(
        "CAST(key AS STRING)", "to_json(struct(*)) AS value"
    )
    .writeStream.outputMode("complete")
    .format("kafka")
    .trigger(processingTime=AGGREGATION_TIME)
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("topic", "rides_all")
    .option("checkpointLocation", "/tmp/checkpoint")
    .start()
)


spark.streams.awaitAnyTermination()
