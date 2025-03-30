terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "your-gcp-project-id"
  region  = "us-central1"
}

resource "google_cloud_run_service" "llm_analysis" {
  name     = "llm-analysis-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/your-gcp-project-id/llm-analysis-service"
        env {
          name  = "OPENAI_API_KEY"
          value = "your-openai-api-key"
        }
      }
    }
  }
}

resource "google_cloud_run_service" "negative_feedback" {
  name     = "negative-feedback-handler"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/your-gcp-project-id/negative-feedback-handler"
        env {
          name  = "SENDGRID_API_KEY"
          value = "your-sendgrid-api-key"
        }
      }
    }
  }
}
