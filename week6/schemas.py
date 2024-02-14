from pyspark.sql import types as T

dispatch_schema = T.StructType(
    [
        T.StructField("dispatching_base_num", T.StringType()),
        T.StructField("pickup_datetime", T.TimestampType()),
        T.StructField("dropOff_datetime", T.TimestampType()),
        T.StructField("PUlocationID", T.StringType()),
        T.StructField("DOlocationID", T.StringType()),
        T.StructField("SR_Flag", T.StringType()),
        T.StructField("Affiliated_base_number", T.StringType()),
    ]
)

ride_schema = T.StructType(
    [
        T.StructField("VendorID", T.IntegerType()),
        T.StructField("lpep_pickup_datetime", T.TimestampType()),
        T.StructField("lpep_dropoff_datetime", T.TimestampType()),
        T.StructField("store_and_fwd_flag", T.StringType()),
        T.StructField("RatecodeID", T.IntegerType()),
        T.StructField("PULocationID", T.IntegerType()),
        T.StructField("DOLocationID", T.IntegerType()),
        T.StructField("passenger_count", T.IntegerType()),
        T.StructField("trip_distance", T.FloatType()),
        T.StructField("fare_amount", T.FloatType()),
        T.StructField("extra", T.FloatType()),
        T.StructField("mta_tax", T.FloatType()),
        T.StructField("tip_amount", T.FloatType()),
        T.StructField("tolls_amount", T.FloatType()),
        T.StructField("ehail_fee", T.FloatType()),
        T.StructField("improvement_surcharge", T.FloatType()),
        T.StructField("total_amount", T.FloatType()),
        T.StructField("payment_type", T.IntegerType()),
        T.StructField("trip_type", T.IntegerType()),
        T.StructField("congestion_surcharge", T.FloatType()),
    ]
)

ALL_RIDE_SCHEMA = T.StructType(
    [
        T.StructField("PUlocationID", T.StringType()),
        T.StructField("DOlocationID", T.StringType()),
    ]
)
