from datetime import timedelta

import pandas as pd
from prefect import flow, task, serve
from prefect.tasks import task_input_hash


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def extract(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    return df


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def load(df: pd.DataFrame, path: str):
    df = df.to_parquet(path, compression="gzip")


@flow(log_prints=True)
def etl_taxi():
    color = "green"
    year = 2020
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    print(f"Downloading {url}...")
    df = extract(url)

    print(f"Number of rows and cols: {df.shape}")
    print(f"Columns: {df.columns}")

    # load onto GCS
    gcs_path = f"gs://pablo-does-zoomcamp/{dataset_file}.parquet"
    load(df, gcs_path)

    return df


if __name__ == "__main__":
    etl_taxi()
