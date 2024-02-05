terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  credentials = file("zoomcamp-412215-985905e8be3a.json")
  project     = "zoomcamp-412215"
  region      = "europe-west1"
  zone        = "europe-west1-b"
}

resource "google_storage_bucket" "static" {
  name          = var.bucket-name
  location      = "EU"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "zoomcamp_dataset"
  friendly_name               = "zoomy"
  description                 = "Dataset for the data-engineering course"
  location                    = "EU"
  default_table_expiration_ms = 3600000
}

