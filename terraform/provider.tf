terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.7.0"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "current" {}
