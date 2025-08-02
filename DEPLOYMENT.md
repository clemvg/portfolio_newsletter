# Deployment and Testing Guide

This guide will walk you through deploying and testing your nightly job. All commands should be run from the **root directory** of the project.

## Prerequisites

Before you begin, make sure you have the following tools installed:
- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/install)
- [Docker](https://docs.docker.com/get-docker/)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## Step 1: Configure Your Environment

1.  **Authenticate with Google Cloud:**
    Open your terminal and run:
    ```bash
    gcloud auth login
    gcloud auth application-default login
    ```

2.  **Set your Project ID:**
    This is already set in `terraform/terraform.tfvars`, but it's good practice to ensure your `gcloud` CLI is configured to the correct project. Replace `your-gcp-project-id` with your actual GCP project ID from the `.tfvars` file.
    ```bash
    gcloud config set project your-gcp-project-id
    ```

3.  **Enable Required APIs:**
    This command enables all the necessary services for the project.
    ```bash
    gcloud services enable \
      run.googleapis.com \
      cloudscheduler.googleapis.com \
      artifactregistry.googleapis.com \
      cloudbuild.googleapis.com
    ```

## Step 2: Deploy Infrastructure and Push Image

1.  **Initialize Terraform:**
    This command prepares Terraform by downloading the necessary Google Cloud provider plugins.
    ```bash
    terraform -chdir=terraform init
    ```

2.  **Apply the Terraform Configuration (First Time):**
    Run the `apply` command. It will create the Artifact Registry repository that we need in the next step. It may fail on the Cloud Run Job since the image doesn't exist yet, which is expected.
    ```bash
    terraform -chdir=terraform apply
    ```
    Review the plan and type `yes` when prompted.

3.  **Configure Docker Authentication:**
    This command tells your local Docker client how to authenticate with your private Artifact Registry.
    ```bash
    gcloud auth configure-docker $(terraform -chdir=terraform output -raw region)-docker.pkg.dev
    ```

4.  **Build the Docker Image:**
    This command builds your Docker image using the `Dockerfile` in the project root.
    ```bash
    docker build -t $(terraform -chdir=terraform output -raw image_path) .
    ```

5.  **Push the Docker Image:**
    Now, push the tagged image to your private repository.
    ```bash
    docker push $(terraform -chdir=terraform output -raw image_path)
    ```

## Step 3: Deploy the Cloud Run Job

1.  **Apply Terraform Again:**
    Run `apply` one more time. This time, Terraform will see that the repository and image now exist, and it will create or update the Cloud Run Job.
    ```bash
    terraform -chdir=terraform apply
    ```
    Review the (much smaller) plan and type `yes` when prompted.

## Step 4: Test the Cloud Run Job

You can trigger the job manually to test it immediately.

1.  **Run the job from the command line:**
    ```bash
    gcloud run jobs execute $(terraform -chdir=terraform output -raw job_name) --region $(terraform -chdir=terraform output -raw region)
    ```

2.  **Check the Logs:**
    Go to the Cloud Run section of the Google Cloud Console, find your job (e.g., `portfolio-newsletter-job-dev`), and inspect its logs. You should see the output from the Python script, including "Job finished."
