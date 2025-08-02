# --- Google Secret Manager ---
# This file is reserved for managing secrets.
#
# As an example, you might create secrets for API keys or database passwords:
#
# resource "google_secret_manager_secret" "api_key" {
#   secret_id = "my-api-key"
#   replication {
#     auto {}
#   }
# }
#
# resource "google_secret_manager_secret_version" "api_key_version" {
#   secret      = google_secret_manager_secret.api_key.id
#   secret_data = var.my_api_key
# }
#
# You would then add `my_api_key` to variables.tf and inject it into the
# Cloud Run job in cloud_run.tf.
