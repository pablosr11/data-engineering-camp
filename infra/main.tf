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

