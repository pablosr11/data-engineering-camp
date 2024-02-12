-- What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)?
SELECT count(tripid) 
FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.fact_trips` 
WHERE EXTRACT(YEAR FROM pickup_datetime AT TIME ZONE "UTC") in (2019,2020)

-- What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos?
WITH gg as (
  SELECT count(service_type) cc, service_type
  FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.fact_trips` 
  WHERE EXTRACT(YEAR FROM pickup_datetime AT TIME ZONE "UTC") in (2019,2020)
  GROUP BY service_type
)
select 
  round(cc/sum(cc) over () * 100,2), service_type
from gg

-- What is the count of records in the model stg_fhv_tripdata after running all models with the test run variable disabled (:false)? For 2019
SELECT count(*)
FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.stg_fhv_tripdata`
WHERE EXTRACT(YEAR FROM pickup_datetime AT TIME ZONE "UTC") = 2019


-- What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)?
-- Create a core model for the stg_fhv_tripdata joining with dim_zones. Similar to what we've done in fact_trips, keep only records with known pickup and dropoff locations entries for pickup and dropoff locations. Run it via the CLI without limits (is_test_run: false) and filter records with pickup time in year 2019.
SELECT count(*)
FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.fact_fhv_trips`
WHERE EXTRACT(YEAR FROM pickup_datetime AT TIME ZONE "UTC") = 2019


-- What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table?
WITH trips_by_month AS (
SELECT 
  EXTRACT(MONTH FROM pickup_datetime AT TIME ZONE "UTC") as month, 
  count(*) as n_trips
FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.fact_fhv_trips`
GROUP BY EXTRACT(MONTH FROM pickup_datetime AT TIME ZONE "UTC")
)
SELECT month, n_trips
FROM trips_by_month
order by n_trips desc
limit 1