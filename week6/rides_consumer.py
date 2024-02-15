import os

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import SparkSession
from schemas import ALL_RIDE_SCHEMA, dispatch_schema, ride_schema

os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell"
)


def sink_console(df, output_mode: str = "complete", processing_time: str = "5 seconds"):
    query = (
        df.writeStream.outputMode(output_mode)
        .trigger(processingTime=processing_time)
        .format("console")
        .option("truncate", False)
        .start()
        .awaitTermination()
    )
    return query  # pyspark.sql.streaming.StreamingQuery


def op_groupby(df, column_names):
    df_aggregation = df.groupBy(column_names).count()
    return df_aggregation


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


df_trip_count_by_pulocation = df.groupBy(["PUlocationID"]).count()


df_pu_location_count = df_trip_count_by_pulocation.sort(F.col("count").desc()).limit(10)
(
    df_pu_location_count.writeStream.outputMode("complete")
    .trigger(processingTime=AGGREGATION_TIME)
    .format("console")
    .start()
)

spark.streams.awaitAnyTermination()
