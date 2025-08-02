# --- Cloud Scheduler ---
# Create a scheduler job to trigger the Cloud Run job every night.

resource "google_cloud_scheduler_job" "nightly" {
  name      = "${var.app_name}-trigger-${var.environment}"
  region    = var.region
  # schedule  = "*/1 * * * *" # Runs every 1 minute for testing
  schedule  = "0 3 * * *" # Runs every day at 3:00 AM
  time_zone = "Europe/Brussels"

  http_target {
    uri         = "https://run.googleapis.com/v2/projects/${var.project_id}/locations/${var.region}/jobs/${google_cloud_run_v2_job.portfolio_newsletter.name}:run"
    http_method = "POST"
    oauth_token {
      service_account_email = google_service_account.service_account.email
    }
  }
}
