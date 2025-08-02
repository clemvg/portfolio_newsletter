locals {
  # Construct the full image path that Cloud Run needs.
  # This combines the location, project ID, repository name, and the specific image name.
  # We append ":latest" to always use the most recently pushed image.
  image_path = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.repository_id}/${var.image_name}:latest"
}
