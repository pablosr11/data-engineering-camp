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


SELECT 
  EXTRACT(MONTH FROM pickup_datetime AT TIME ZONE "UTC") as mm, 
  count(*) as count
FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.fact_fhv_trips`
GROUP BY EXTRACT(MONTH FROM pickup_datetime AT TIME ZONE "UTC")