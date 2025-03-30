#!/bin/bash

PROJECT_ID="your-gcp-project-id"
REGION="us-central1"

# Déploiement du service LLM Analysis
gcloud builds submit --tag gcr.io/$PROJECT_ID/llm-analysis-service ./llm_analysis_service
gcloud run deploy llm-analysis-service --image gcr.io/$PROJECT_ID/llm-analysis-service --platform managed --region $REGION --allow-unauthenticated

# Déploiement du service Negative Feedback Handler
gcloud builds submit --tag gcr.io/$PROJECT_ID/negative-feedback-handler ./negative_feedback_handler
gcloud run deploy negative-feedback-handler --image gcr.io/$PROJECT_ID/negative-feedback-handler --platform managed --region $REGION --allow-unauthenticated
