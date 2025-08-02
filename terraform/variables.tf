variable "project_id" {
  description = "The Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "The Google Cloud region to deploy resources in."
  type        = string
  default     = "europe-west1"
}

variable "image_name" {
  description = "The name of the Docker image in Artifact Registry (e.g., 'portfolio-newsletter-image')."
  type        = string
}

variable "app_name" {
  description = "A base name for the application's resources (Cloud Run Job, Service Account, etc.)."
  type        = string
  default     = "portfolio-newsletter"
}

variable "environment" {
  description = "The deployment environment (e.g., dev, acc, pro)."
  type        = string
  default     = "dev"
}

variable "tickers" {
  description = "A comma-separated list of stock tickers for the newsletter."
  type        = string
  default     = "AAPL,GOOGL,MSFT"
}

