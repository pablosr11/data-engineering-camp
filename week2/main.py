from datetime import timedelta
from enum import Enum

import pandas as pd
from prefect import flow, serve, task
from prefect.tasks import task_input_hash


class Color(Enum):
    GREEN = "green"
    YELLOW = "yellow"


class Year(Enum):
    YEAR_2019 = 2019
    YEAR_2020 = 2020


class Month(Enum):
    JAN = "01"
    FEB = "02"
    MAR = "03"
    NOV = "11"


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def extract(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    return df


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def load(df: pd.DataFrame, path: str):
    df = df.to_parquet(path, compression="gzip")


@flow(log_prints=True)
def etl_taxi_data_gh_to_gcs(
    color: Color = Color.GREEN, year: Year = Year.YEAR_2019, month: Month = Month.JAN
):
    dataset_file = f"{color.value}_tripdata_{year}-{month:02}"
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color.value}/{dataset_file}.csv.gz"

    print(f"Downloading {url}...")
    df = extract(url)

    print(f"Number of rows and cols: {df.shape}")
    print(f"Columns: {df.columns}")

    # load onto GCS
    gcs_path = f"gs://pablo-does-zoomcamp/{dataset_file}.parquet"
    load(df, gcs_path)
    print(f"Data saved to {gcs_path}")

    return df


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def extract_from_gcs(filepath: str) -> pd.DataFrame:
    return pd.read_parquet(filepath)


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def load_to_bq(df: pd.DataFrame, dataset: str, table: str, project_id: str):
    df.to_gbq(
        destination_table=f"{dataset}.{table}",
        project_id=project_id,
        if_exists="append",
    )


@flow(log_prints=True)
def etl_taxi_data_gcs_to_bq(
    color: Color,
    year: Year,
    month: Month,
    dataset: str = "zoomcamp_dataset",
    table: str = "events",
    project_id: str = "zoomcamp-412215",
):

    dataset_file = f"{color.value}_tripdata_{year.value}-{month.value:02}"
    filepath = f"gs://pablo-does-zoomcamp/{dataset_file}.parquet"
    print(f"Extracting {filepath}...")

    # extract from GCS
    df = extract_from_gcs(filepath)

    # only keep trip_distance,fare_amount and VendorID
    df = df[["trip_distance", "fare_amount", "VendorID"]]

    print(f"Number of rows and cols: {df.shape}")

    print("Loading into BQ...")

    load_to_bq(df, dataset, table, project_id)


@flow(log_prints=True)
def row_counter_flow_from_gh(color: Color, year: Year, month: Month):
    dataset_file = f"{color.value}_tripdata_{year.value}-{month.value:02}"
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color.value}/{dataset_file}.csv.gz"

    print(f"Downloading {url}...")
    df = extract(url)

    print(f"Number of rows and cols: {df.shape}")
    print(f"Columns: {df.columns}")


if __name__ == "__main__":
    gb_to_gcs = etl_taxi_data_gh_to_gcs.to_deployment("gh_to_gcs")
    gcs_to_bq = etl_taxi_data_gcs_to_bq.to_deployment("gcs_to_bq")
    serve(gcs_to_bq, gb_to_gcs)

    # Deploy from GH
    # prefect deployment build week2/main.py:row_counter_flow_from_gh --name row_counter --tag 'gh-block' -sb github/gh-block -a

    # Local agent
    # prefect agent start --pool "default-agent-pool"
