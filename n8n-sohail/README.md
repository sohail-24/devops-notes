# DevOps AI Control Plane using n8n – Complete Setup Notes

Author: Mohammed Sohail
Purpose: Build an AI-powered DevOps monitoring system using n8n that watches ArgoCD deployments, analyzes Kubernetes failures, and sends Gmail alerts.

---

# 1. System Overview

The system automates DevOps incident monitoring.

Architecture Flow:

ArgoCD Event
↓
Webhook Trigger (n8n)
↓
Fetch ArgoCD API logs
↓
Fetch Kubernetes pod logs
↓
AI Analysis (OpenAI / Ollama)
↓
Send Gmail Notification

When a deployment fails, the system automatically:

1. Receives a webhook from ArgoCD
2. Fetches logs from Kubernetes
3. Sends logs to an AI model for analysis
4. Sends a summarized alert to Gmail

---

# 2. Tools Used

n8n – automation engine
Docker – run services locally
PostgreSQL – store workflow executions
Redis – queue system for scaling
ArgoCD – GitOps deployment system
Kubernetes – container orchestration
OpenAI / Ollama – AI log analysis
Gmail SMTP – send alerts

---

# 3. Project Directory Structure

Create a folder:

devops-ai-control-plane

Inside it place:

README.md
docker-compose.yml
.env.example
devops_ai_control_plane_workflow.json
argocd-webhook-config.yaml
gmail-smtp-config.md
security-recommendations.md

k8s-manifests/

Inside k8s-manifests:

01-namespace.yaml
02-secrets.yaml
03-configmap.yaml
04-postgres.yaml
05-redis.yaml
06-n8n-deployment.yaml
07-n8n-worker.yaml
08-rbac.yaml
09-ingress.yaml

---

# 4. Prerequisites

Install the following tools.

Docker
Docker Compose
kubectl
Git

Check installation:

docker --version
docker compose version
kubectl version --client

---

# 5. Local Setup (Recommended First Step)

Create the project folder:

mkdir devops-ai-control-plane
cd devops-ai-control-plane

Copy the generated files from Kimi.

---

# 6. Environment Configuration

Create environment file:

cp .env.example .env

Edit:

nano .env

Add your credentials.

Example:

OPENAI_API_KEY=your_api_key

GMAIL_USER=[your_email@gmail.com](mailto:your_email@gmail.com)

GMAIL_APP_PASSWORD=your_app_password

ARGOCD_TOKEN=your_argocd_token

POSTGRES_USER=n8n

POSTGRES_PASSWORD=n8npassword

POSTGRES_DB=n8n

REDIS_HOST=redis

---

# 7. Start the Platform

Run Docker stack:

docker compose up -d

Containers started:

n8n
postgres
redis

Check containers:

docker ps

---

# 8. Access n8n UI

Open browser:

http://localhost:5678

First login may ask for account creation.

---

# 9. Import the Workflow

Inside n8n UI:

Workflows
→ Import from file
→ Select

devops_ai_control_plane_workflow.json

Activate the workflow.

---

# 10. Configure Credentials in n8n

Open workflow nodes and configure credentials.

Gmail configuration:

SMTP Host:

smtp.gmail.com

Port:

587

Username:

your Gmail

Password:

Gmail App Password

---

# 11. Configure AI Analysis

Option A – OpenAI

Add credential:

OPENAI_API_KEY

Option B – Local AI (recommended later)

Use Ollama API:

http://localhost:11434

---

# 12. Connect ArgoCD Webhook

Apply webhook configuration:

kubectl apply -f argocd-webhook-config.yaml

Add annotation to applications.

Example:

metadata:
annotations:
notifications.argoproj.io/subscribe.on-sync-failed.n8n: ""
notifications.argoproj.io/subscribe.on-health-degraded.n8n: ""

---

# 13. Webhook Endpoint

n8n exposes webhook:

Local:

http://localhost:5678/webhook/argo-events

Docker internal:

http://n8n:5678/webhook/argo-events

Kubernetes production:

https://n8n.yourdomain.com/webhook/argo-events

---

# 14. Test the System

Send test webhook.

curl -X POST 
-H "Content-Type: application/json" 
-d '{
"type": "sync-failed",
"application": "test-app",
"namespace": "default",
"syncStatus": "OutOfSync",
"healthStatus": "Degraded",
"operationPhase": "Failed"
}' 
http://localhost:5678/webhook/argo-events

Expected result:

Gmail alert with AI analysis.

---

# 15. Deploy to Kubernetes (Production)

Apply manifests.

kubectl apply -f k8s-manifests/01-namespace.yaml
kubectl apply -f k8s-manifests/02-secrets.yaml
kubectl apply -f k8s-manifests/03-configmap.yaml

Deploy databases.

kubectl apply -f k8s-manifests/04-postgres.yaml
kubectl apply -f k8s-manifests/05-redis.yaml

Deploy n8n.

kubectl apply -f k8s-manifests/06-n8n-deployment.yaml
kubectl apply -f k8s-manifests/07-n8n-worker.yaml

Configure access.

kubectl apply -f k8s-manifests/08-rbac.yaml
kubectl apply -f k8s-manifests/09-ingress.yaml

---

# 16. Monitoring

n8n exposes metrics:

/metrics endpoint

Prometheus can scrape this.

Metrics examples:

n8n_executions_total
n8n_execution_duration_seconds
n8n_executions_failed_total

---

# 17. Troubleshooting

Webhook not triggering

Check:

WEBHOOK_URL variable

AI analysis failing

Check:

OPENAI_API_KEY

Email not sending

Check:

Gmail App Password

Kubernetes logs failing

Check RBAC permissions.

---

# 18. Scaling

Use n8n worker pods.

HorizontalPodAutoscaler example:

Min replicas: 2
Max replicas: 10
CPU threshold: 70%

---

# 19. Final Result

Your system becomes a DevOps AI monitoring platform.

Example incident:

ArgoCD sync fails
↓
Webhook triggers n8n
↓
Logs fetched
↓
AI analyzes error
↓
Gmail alert sent

---

# 20. Future Improvements

Add Telegram alerts
Add Slack alerts
Use Ollama for local AI
Add automatic remediation
Add CI/CD monitoring

---

End of Notes
