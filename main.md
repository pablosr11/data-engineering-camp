# Data Engineering ZoomCamp 2023


## Week 1

### Create a docker container for postgres. Obvs obfuscate password rest of details. Local dir is mounted for persistence.
```bash
docker run -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=zoomcamp -d -v ./pgdata:/var/lib/postgresql/data postgres:latest
```
