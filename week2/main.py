from datetime import timedelta
from enum import Enum

import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash


class Color(Enum):
    GREEN = "green"
    YELLOW = "yellow"


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def extract(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    return df


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def load(df: pd.DataFrame, path: str):
    df = df.to_parquet(path, compression="gzip")


@flow(log_prints=True)
def etl_load_taxi_data(color: Color = Color.GREEN, year: int = 2020, month: int = 1):
    dataset_file = f"{color.value}_tripdata_{year}-{month:02}"
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color.value}/{dataset_file}.csv.gz"

    print(f"Downloading {url}...")
    df = extract(url)

    print(f"Number of rows and cols: {df.shape}")
    print(f"Columns: {df.columns}")

    # load onto GCS
    gcs_path = f"gs://pablo-does-zoomcamp/{dataset_file}.parquet"
    load(df, gcs_path)

    return df


if __name__ == "__main__":
    etl_load_taxi_data.serve("etl-taxi-to-gcs", cron="0 5 1 * *")
