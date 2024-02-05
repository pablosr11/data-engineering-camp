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
  name     = var.bucket-name
  location = "EU"

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = "zoomcamp_dataset"
  location   = "EU"
  project    = "zoomcamp-412215"
}

