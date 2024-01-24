provider "google" {
  project = "zoomcamp"
  region  = "europe-west1"
}

resource "google_storage_bucket" "static" {
  name          = var.bucket-name
  location      = "EU"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
}

resource "google_service_account" "bqowner" {
  account_id = "bqowner"
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "zoomcamp_dataset"
  friendly_name               = "zoomy"
  description                 = "Dataset for the data-engineering course"
  location                    = "EU"
  default_table_expiration_ms = 3600000

  labels = {
    env = "default"
  }

  access {
    role          = "OWNER"
    user_by_email = google_service_account.bqowner.email
  }

  access {
    role   = "READER"
    domain = "psiesta.com"
  }
}
