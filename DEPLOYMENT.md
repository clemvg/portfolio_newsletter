# Deployment and Testing Guide

This guide will walk you through deploying and testing your portfolio newsletter Cloud Run Job. The application runs as a scheduled batch job that generates newsletters for configured stock tickers. All commands should be run from the **root directory** of the project.

Note that this project is deployed on a sandbox GCP project sponsored by ML6.

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

3.  **Configure Terraform Variables (Optional but Recommended):**
    Create a `terraform/terraform.tfvars` file to avoid manual input during deployment. This file should contain your actual values:
    ```bash
    # terraform/terraform.tfvars
    project_id = "your-gcp-project-id"
    region = "europe-west1"
    image_name = "portfolio-newsletter-image-v_0"
    app_name = "portfolio-newsletter"
    environment = "dev"
    tickers = "AAPL,GOOGL,MSFT"
    email_recipients = "your-email@example.com"
    gmail_user = "your-gmail@gmail.com"
    gmail_app_password = "your-app-password-here"
    ```
    **Note:** Replace the placeholder values with your actual Gmail credentials and email addresses.

4.  **Enable Required APIs:**
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
    **Note:** If you created a `terraform.tfvars` file, Terraform will automatically use those values. Otherwise, you'll be prompted to enter the variable values manually.
    Review the plan and type `yes` when prompted.

3.  **Configure Docker Authentication (One-time setup):**
    This command tells your local Docker client how to authenticate with your private Artifact Registry. This only needs to be run once per machine.
    ```bash
    gcloud auth configure-docker $(terraform -chdir=terraform output -raw region)-docker.pkg.dev
    ```

4.  **Build the Docker Image:**
    This command builds your Docker image using the `Dockerfile` in the `app/` directory.
    ```bash
    docker build -t $(terraform -chdir=terraform output -raw image_path) app/
    ```
    Or if you are on an Apple silicon chip, Cloud Run requires amd64/linux architecture so build with:
    ```bash
    docker build --platform linux/amd64 -t $(terraform -chdir=terraform output -raw image_path) app/
    ```

5.  **Push the Docker Image:**
    Now, push the tagged image to your private repository.
    ```bash
    docker push $(terraform -chdir=terraform output -raw image_path)
    ```

    Your image can now be seen in your `Artifact Registry`.

## Step 3: Deploy the Cloud Run Job

1.  **Apply Terraform Again:**
    Run `apply` one more time. This time, Terraform will see that the repository and image now exist, and it will create or update the Cloud Run Job.
    ```bash
    terraform -chdir=terraform apply
    ```
    **Note:** Terraform will automatically use values from `terraform.tfvars` if present, or prompt for manual input if not.
    Review the (much smaller) plan and type `yes` when prompted.

## Step 4: Test the Cloud Run Job

You can trigger the job manually to test it immediately.

1.  **Run the job from the command line:**
    ```bash
    gcloud run jobs execute $(terraform -chdir=terraform output -raw job_name) --region $(terraform -chdir=terraform output -raw region)
    ```

2.  **Check the Logs:**
    Go to the Cloud Run section of the Google Cloud Console, find under the `Jobs` section your job (e.g., `portfolio-newsletter-job-dev`), and inspect its logs. You should see the output from the Python script, including "Job finished."


## Step 5: Destroy the Infrastructure

When you are done, you can remove all Terraform-managed resources (Cloud Run Job, Scheduler, Artifact Registry repository, IAM bindings, etc.). Run this from the project root:

1. Destroy with Terraform:
    ```bash
    terraform -chdir=terraform destroy
    ```
    Review the plan and type `yes` when prompted. To skip the prompt, use:
    ```bash
    terraform -chdir=terraform destroy -auto-approve
    ```

2. Optional local cleanup:
    - Remove the locally built Docker image tag used for deployment:
      ```bash
      docker rmi $(terraform -chdir=terraform output -raw image_path) || true
      ```
    - If you want a completely clean local Terraform directory (not required):
      ```bash
      rm -rf terraform/.terraform terraform/terraform.tfstate*
      ```

3. Optional: disable previously enabled APIs (you can re-enable later if needed):
    ```bash
    gcloud services disable \
      run.googleapis.com \
      cloudscheduler.googleapis.com \
      artifactregistry.googleapis.com \
      cloudbuild.googleapis.com \
      --force
    ```

