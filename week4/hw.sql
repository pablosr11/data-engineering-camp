SELECT 
  EXTRACT(MONTH FROM pickup_datetime AT TIME ZONE "UTC") as mm, 
  count(*) as count
FROM `zoomcamp-412215.zoomcamp_dataset_dbt_psand.fact_fhv_trips`
GROUP BY EXTRACT(MONTH FROM pickup_datetime AT TIME ZONE "UTC")