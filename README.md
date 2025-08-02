# Portfolio Newsletter GCP Project

This project uses Terraform to deploy a serverless infrastructure on Google Cloud Platform (GCP). The goal is to run a nightly job that executes a Python script.

The infrastructure consists of:
- **Cloud Run:** A serverless job to execute the Python application.
- **Cloud Scheduler:** A cron job trigger to run the Cloud Run job on a nightly schedule.
- **Artifact Registry:** A private Docker container registry to store the application image.
- **IAM:** A dedicated Service Account with the principle of least privilege.

For detailed deployment steps, please see `DEPLOYMENT.md`.
