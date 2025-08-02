# --- Cloud Run Job ---
# Define the job that will run the container on a schedule.

resource "google_cloud_run_v2_job" "portfolio_newsletter" {
  name     = "${var.app_name}-job-${var.environment}"
  location = var.region

  template {
    template {
      containers {
        image = local.image_path

        env {
          name  = "TICKERS"
          value = var.tickers
        }

        env {
          name  = "EMAIL_RECIPIENTS"
          value = var.email_recipients
        }

        env {
          name  = "GMAIL_USER"
          value = var.gmail_user
        }

        env {
          name  = "GMAIL_APP_PASSWORD"
          value = var.gmail_app_password
        }


      }
      service_account = google_service_account.service_account.email
      timeout         = "3600s"
    }
    parallelism = 1
    task_count  = 1
  }
}
