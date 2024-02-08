SELECT count(pickup_datetime) FROM `zoomcamp-412215.zoomcamp_dataset.native_fhv_tripdata` LIMIT 1000

SELECT count(pickup_datetime) FROM `zoomcamp-412215.zoomcamp_dataset.fhv_tripdata` LIMIT 1000

-- # Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.
SELECT DISTINCT(Affiliated_base_number) FROM `zoomcamp-412215.zoomcamp_dataset.native_fhv_tripdata`

SELECT DISTINCT(Affiliated_base_number) FROM `zoomcamp-412215.zoomcamp_dataset.fhv_tripdata`

