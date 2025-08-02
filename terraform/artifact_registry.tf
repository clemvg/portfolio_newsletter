# --- Artifact Registry ---
# Create a repository to store the Docker image for the Cloud Run job.

resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "${var.app_name}-repo-${var.environment}"
  format        = "DOCKER"
  description   = "Repository for cloud run images"
}
