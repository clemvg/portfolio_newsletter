# --- Service Account & IAM ---

# Creates a service account for the Cloud Run job to run as.
resource "google_service_account" "service_account" {
  account_id   = "${var.app_name}-sa-${var.environment}"
  display_name = "Service Account for ${var.app_name} (${var.environment})"
}

# Grant the service account permission to be able to trigger THIS specific Cloud Run job.
# The Cloud Scheduler uses this service account's identity to make the request.
resource "google_cloud_run_v2_job_iam_member" "job_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_job.portfolio_newsletter.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_service_account_iam_member" "scheduler_token_creator" {
  service_account_id = google_service_account.service_account.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:service-${data.google_project.current.number}@gcp-sa-cloudscheduler.iam.gserviceaccount.com"
}
