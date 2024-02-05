terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
  backend "gcs" {
    bucket = "73572d6977e97d93-bucket-tfstate"
    prefix = "terraform/state"
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
  dataset_id  = "zoomcamp_dataset"
  location    = "EU"
  project     = "zoomcamp-412215"
  description = "Dataset for the data-engineering course"
}

resource "random_id" "bucket_prefix" {
  byte_length = 8
}

resource "google_storage_bucket" "default" {
  name          = "${random_id.bucket_prefix.hex}-bucket-tfstate"
  force_destroy = false
  location      = "EU"
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }

}

