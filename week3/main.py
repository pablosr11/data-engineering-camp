from datetime import timedelta
from io import BytesIO

import httpx
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket


@task(cache_expiration=timedelta(days=1), cache_key_fn=task_input_hash)
def download_file_from_gh_push_to_gcs(url: str):
    # download from url
    # upload to f"gs://pablo-does-zoomcamp/"

    filename = url.split("/")[-1]

    gcp_cloud_storage_bucket_block = GcsBucket.load("gcs-bucket")

    with httpx.Client() as client:
        print(f"Downloading {url}...")
        response = client.get(url, follow_redirects=True)
        response.raise_for_status()
        file_object = BytesIO(response.content)
        print(len(response.content))
        print(f"Uploading {filename} to GCS...")
        gcp_cloud_storage_bucket_block.upload_from_file_object(file_object, filename)
        print(f"\n=== Uploaded {filename} to GCS")


@flow(log_prints=True)
def load_gh_to_gcs():

    list_of_files = [
        "fhv_tripdata_2019-01.csv.gz",
        "fhv_tripdata_2019-02.csv.gz",
        "fhv_tripdata_2019-03.csv.gz",
        "fhv_tripdata_2019-04.csv.gz",
        "fhv_tripdata_2019-05.csv.gz",
        "fhv_tripdata_2019-06.csv.gz",
        "fhv_tripdata_2019-07.csv.gz",
        "fhv_tripdata_2019-08.csv.gz",
        "fhv_tripdata_2019-09.csv.gz",
        "fhv_tripdata_2019-10.csv.gz",
        "fhv_tripdata_2019-11.csv.gz",
        "fhv_tripdata_2019-12.csv.gz",
    ]
    tasks = []
    for f in list_of_files:
        url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{f}"
        tasks.append(download_file_from_gh_push_to_gcs.submit(url))

    return tasks


if __name__ == "__main__":
    load_gh_to_gcs()
