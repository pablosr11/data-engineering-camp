

{{ config(
    materialized='view'
) }}
SELECT * FROM {{
     source('staging', 'green_tripdata_all') }}
LIMIT 100