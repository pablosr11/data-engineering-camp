
{{
    config(
        materialized='table'
    )
}}

with dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
),
fhv_trips as (
    select * 
    from {{ ref('stg_fhv_tripdata') }}
    where pickup_locationid IS NOT NULL 
    AND dropoff_locationid IS NOT NULL 
)
select fhv_trips.*,
    pickup_zone.borough as pickup_borough,
    pickup_zone.zone as pickup_zone,
    dropoff_zone.borough as dropoff_borough,
    dropoff_zone.zone as dropoff_zone
from fhv_trips
    inner join dim_zones as pickup_zone on fhv_trips.pickup_locationid = pickup_zone.locationid
    inner join dim_zones as dropoff_zone on fhv_trips.dropoff_locationid = dropoff_zone.locationid