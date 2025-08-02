# --- Outputs ---

output "job_name" {
  value = google_cloud_run_v2_job.portfolio_newsletter.name
}

output "artifact_registry_repository" {
  value = google_artifact_registry_repository.repo.name
}

output "region" {
  description = "The region where the resources are deployed."
  value       = var.region
}

output "image_path" {
  description = "The full path to the container image in Artifact Registry."
  value       = local.image_path
}
