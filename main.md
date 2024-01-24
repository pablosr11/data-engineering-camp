# Data Engineering ZoomCamp 2023


## Week 1

### Create a docker container for postgres. Obvs obfuscate password rest of details. Local dir is mounted for persistence.
```bash
docker run -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=zoomcamp -d -v ./pgdata:/var/lib/postgresql/data postgres:latest
```

### Create tables. Quick copypaste from formatter based on csv.
```sql
CREATE TABLE zones (
    LocationID INT,
    Borough VARCHAR(50),
    Zone VARCHAR(255),
    service_zone VARCHAR(50)
);

CREATE TABLE trips (
    VendorID INT,
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    store_and_fwd_flag CHAR(1),
    RatecodeID INT,
    PULocationID INT,
    DOLocationID INT,
    passenger_count INT,
    trip_distance FLOAT,
    fare_amount FLOAT,
    extra FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    ehail_fee FLOAT,  -- Assuming it's a float, adjust if different
    improvement_surcharge FLOAT,
    total_amount FLOAT,
    payment_type INT,
    trip_type INT,
    congestion_surcharge FLOAT
);
```

### Copy data into tables.
```bash
psql -h localhost -U postgres -d zoomcamp -c "\COPY zones FROM '/Users/ps/repos/learnings/data-engineering-camp/taxi+_zone_lookup.csv' DELIMITER ',' CSV HEADER;"
psql -h localhost -U postgres -d zoomcamp -c "\COPY trips FROM '/Users/ps/repos/learnings/data-engineering-camp/green_tripdata_2019-01.csv' DELIMITER ',' CSV HEADER;"
```
