{{ config(
    materialized='table',
    unique_key='zone_id',
    sort='zone_id'
) }}
select 
    locationid,
    borough,
    zone,
    replace(service_zone, 'Boro', 'Green') as service_zone
from {{ ref('taxi_zone_lookup')}}