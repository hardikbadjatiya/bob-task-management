#!/bin/bash
set -e

PROJECT_ID="hardik-prompt-wars"
REGION="us-central1"

echo "====================================="
echo "Starting Quick GCP Deployment (SQLite & No Redis) for Bob Task Management"
echo "====================================="

# 1. Deploy Backend
echo "[1/2] Deploying Backend to Cloud Run..."
cd /Users/hardik/Downloads/bob-task-management/backend
gcloud run deploy task-backend-quick --source . \
  --region=$REGION \
  --project=$PROJECT_ID \
  --allow-unauthenticated \
  --port=8000 \
  --set-env-vars="DATABASE_URL=sqlite:////tmp/sql_app.db,SECRET_KEY=production_secret_key"

BACKEND_URL=$(gcloud run services describe task-backend-quick --region=$REGION --project=$PROJECT_ID --format="value(status.url)")
echo "Backend deployed at $BACKEND_URL"

# 2. Deploy Frontend
echo "[2/2] Deploying Frontend to Cloud Run..."
cd /Users/hardik/Downloads/bob-task-management/frontend
gcloud run deploy task-frontend-quick --source . \
  --region=$REGION \
  --project=$PROJECT_ID \
  --allow-unauthenticated \
  --port=3000 \
  --set-env-vars="VITE_API_URL=$BACKEND_URL/api/v1"

FRONTEND_URL=$(gcloud run services describe task-frontend-quick --region=$REGION --project=$PROJECT_ID --format="value(status.url)")

# 3. Update Backend CORS to allow Frontend Origin
echo "Configuring backend CORS for $FRONTEND_URL..."
gcloud run services update task-backend-quick \
  --region=$REGION \
  --project=$PROJECT_ID \
  --update-env-vars="CORS_ORIGINS=[\"$FRONTEND_URL\"],DATABASE_URL=sqlite:////tmp/sql_app.db,SECRET_KEY=production_secret_key"

echo "====================================="
echo "Quick Deployment Complete! 🚀"
echo "Frontend: $FRONTEND_URL"
echo "Backend: $BACKEND_URL"
echo "====================================="
