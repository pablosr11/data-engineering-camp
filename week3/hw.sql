SELECT count(pickup_datetime) FROM `zoomcamp-412215.zoomcamp_dataset.native_fhv_tripdata` LIMIT 1000

SELECT count(pickup_datetime) FROM `zoomcamp-412215.zoomcamp_dataset.fhv_tripdata` LIMIT 1000

-- # Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.
SELECT DISTINCT(Affiliated_base_number) FROM `zoomcamp-412215.zoomcamp_dataset.native_fhv_tripdata`

SELECT DISTINCT(Affiliated_base_number) FROM `zoomcamp-412215.zoomcamp_dataset.fhv_tripdata`

-- # How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
SELECT COUNT(*) FROM `zoomcamp-412215.zoomcamp_dataset.native_fhv_tripdata` WHERE PUlocationID IS NULL AND DOlocationID IS NULL


-- # filter by pickup_datetime and order by affiliated_base_number?
CREATE TABLE
  `zoomcamp-412215.zoomcamp_dataset.native_part_fhv_tripdata`
PARTITION BY
  DATE(pickup_datetime)
AS (
  SELECT
    *
  FROM
    `zoomcamp-412215.zoomcamp_dataset.native_fhv_tripdata`
);

-- # distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).
SELECT DISTINCT(Affiliated_base_number) FROM `zoomcamp-412215.zoomcamp_dataset.native_fhv_tripdata` WHERE DATE(pickup_datetime) >= '2019-03-01' AND DATE(pickup_datetime)<='2019-03-31'
SELECT DISTINCT(Affiliated_base_number) FROM `zoomcamp-412215.zoomcamp_dataset.native_part_fhv_tripdata` WHERE DATE(pickup_datetime) >= '2019-03-01' AND DATE(pickup_datetime)<='2019-03-31'
