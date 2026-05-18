#!/bin/bash
set -e

PROJECT_ID="hardik-prompt-wars"
REGION="us-central1"

# Generate secure random password for database
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
echo "Generated secure database password"

echo "====================================="
echo "Starting GCP Deployment for Bob Task Management"
echo "====================================="

# 1. Create Cloud SQL Instance
echo "[1/4] Creating Cloud SQL PostgreSQL instance (task-postgres)..."
echo "This might take 5-10 minutes. Running in background."
gcloud sql instances create task-postgres --database-version=POSTGRES_15 --cpu=1 --memory=4GB --region=$REGION --project=$PROJECT_ID --async

# 2. Create Redis Instance
echo "[2/4] Creating Redis instance (task-redis)..."
echo "This might take 5-10 minutes. Running in background."
gcloud redis instances create task-redis --size=1 --region=$REGION --redis-version=redis_7_0 --network=projects/$PROJECT_ID/global/networks/default --project=$PROJECT_ID --async

# Wait for Redis
echo "Waiting for Redis to become READY..."
while true; do
  STATE=$(gcloud redis instances describe task-redis --region=$REGION --project=$PROJECT_ID --format="value(state)" 2>/dev/null || echo "CREATING")
  if [ "$STATE" == "READY" ]; then
    break
  fi
  sleep 20
done
REDIS_IP=$(gcloud redis instances describe task-redis --region=$REGION --project=$PROJECT_ID --format="value(host)")
REDIS_PORT=$(gcloud redis instances describe task-redis --region=$REGION --project=$PROJECT_ID --format="value(port)")
echo "Redis is ready at $REDIS_IP:$REDIS_PORT"

# Wait for Cloud SQL
echo "Waiting for Cloud SQL to become RUNNABLE..."
while true; do
  SQL_STATE=$(gcloud sql instances describe task-postgres --project=$PROJECT_ID --format="value(state)" 2>/dev/null || echo "CREATING")
  if [ "$SQL_STATE" == "RUNNABLE" ]; then
    break
  fi
  sleep 20
done

echo "Configuring Cloud SQL database and user..."
gcloud sql users set-password postgres --instance=task-postgres --password="$DB_PASSWORD" --project=$PROJECT_ID || true
gcloud sql databases create taskdb --instance=task-postgres --project=$PROJECT_ID || true
gcloud sql users create taskuser --instance=task-postgres --password="$DB_PASSWORD" --project=$PROJECT_ID || true

# Store password in Secret Manager for secure access
echo "Storing database password in Secret Manager..."
echo -n "$DB_PASSWORD" | gcloud secrets create task-db-password --data-file=- --project=$PROJECT_ID 2>/dev/null || \
echo -n "$DB_PASSWORD" | gcloud secrets versions add task-db-password --data-file=- --project=$PROJECT_ID

# 3. Deploy Backend
echo "[3/4] Deploying Backend to Cloud Run..."
cd /Users/hardik/Downloads/bob-task-management/backend

# Generate secure SECRET_KEY
SECRET_KEY=$(openssl rand -base64 32)

gcloud run deploy task-backend --source . \
  --region=$REGION \
  --project=$PROJECT_ID \
  --allow-unauthenticated \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:task-postgres \
  --network=default \
  --subnet=default \
  --port=8000 \
  --set-env-vars="DATABASE_URL=postgresql+psycopg2://taskuser:$DB_PASSWORD@/taskdb?host=/cloudsql/$PROJECT_ID:$REGION:task-postgres,REDIS_URL=redis://$REDIS_IP:$REDIS_PORT/0,SECRET_KEY=$SECRET_KEY" \
  --set-secrets="DB_PASSWORD=task-db-password:latest"

BACKEND_URL=$(gcloud run services describe task-backend --region=$REGION --project=$PROJECT_ID --format="value(status.url)")
echo "Backend deployed at $BACKEND_URL"

# 4. Deploy Frontend
echo "[4/4] Deploying Frontend to Cloud Run..."
cd /Users/hardik/Downloads/bob-task-management/frontend
gcloud run deploy task-frontend --source . \
  --region=$REGION \
  --project=$PROJECT_ID \
  --allow-unauthenticated \
  --port=3000 \
  --set-env-vars="VITE_API_URL=$BACKEND_URL"

FRONTEND_URL=$(gcloud run services describe task-frontend --region=$REGION --project=$PROJECT_ID --format="value(status.url)")

echo "====================================="
echo "Deployment Complete! 🚀"
echo "Frontend: $FRONTEND_URL"
echo "Backend: $BACKEND_URL"
echo "====================================="
