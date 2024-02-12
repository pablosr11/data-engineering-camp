-- What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)?
SELECT count(tripid) 
FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.fact_trips` 
WHERE EXTRACT(YEAR FROM pickup_datetime AT TIME ZONE "UTC") in (2019,2020)

SELECT 
  EXTRACT(MONTH FROM pickup_datetime AT TIME ZONE "UTC") as mm, 
  count(*) as count
FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.fact_fhv_trips`
GROUP BY EXTRACT(MONTH FROM pickup_datetime AT TIME ZONE "UTC")