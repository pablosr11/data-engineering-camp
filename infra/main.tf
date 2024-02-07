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
  dataset_id                  = "zoomcamp_dataset"
  location                    = "EU"
  project                     = "zoomcamp-412215"
  description                 = "Dataset for the data-engineering course"
  default_table_expiration_ms = 3600000 // 1 hour
}

resource "google_bigquery_table" "events" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "events"

  schema = <<EOF
[
  {
    "name": "VendorID",
    "type": "STRING"
  },
  {
    "name": "lpep_pickup_datetime",
    "type": "STRING"
  },
  {
    "name": "lpep_dropoff_datetime",
    "type": "STRING"
  },
  {
    "name": "store_and_fwd_flag",
    "type": "STRING"
  },
  {
    "name": "RatecodeID",
    "type": "STRING"
  },
  {
    "name": "PULocationID",
    "type": "STRING"
  },
  {
    "name": "DOLocationID",
    "type": "STRING"
  },
  {
    "name": "passenger_count",
    "type": "STRING"
  },
  {
    "name": "trip_distance",
    "type": "STRING"
  },
  {
    "name": "fare_amount",
    "type": "STRING"
  },
  {
    "name": "extra",
    "type": "STRING"
  },
  {
    "name": "mta_tax",
    "type": "STRING"
  },
  {
    "name": "tip_amount",
    "type": "STRING"
  },
  {
    "name": "tolls_amount",
    "type": "STRING"
  },
  {
    "name": "ehail_fee",
    "type": "STRING"
  },
  {
    "name": "improvement_surcharge",
    "type": "STRING"
  },
  {
    "name": "total_amount",
    "type": "STRING"
  },
  {
    "name": "payment_type",
    "type": "STRING"
  },
  {
    "name": "trip_type",
    "type": "STRING"
  },
  {
    "name": "congestion_surcharge",
    "type": "STRING"
  }
]
EOF
}
