# Better App - Kubernetes Deployment Guide

## Overview
This guide covers deploying the Better App using GitOps practices with ArgoCD on Kubernetes.

## Architecture
- **Application**: Flask web app with SQLite database
- **Container**: Slim Python 3.11 Docker image
- **Database**: StatefulSet with persistent storage
- **Deployment**: Rolling update strategy with 3-5 replicas
- **GitOps**: ArgoCD for continuous deployment
- **CI/CD**: GitHub Actions for automated builds

## Prerequisites
- Kubernetes cluster (1.20+)
- ArgoCD installed
- NGINX Ingress Controller
- cert-manager (for TLS)
- GitHub repository

## Quick Start

### 1. Setup Repository
```bash
# Clone and push to your GitHub repository
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/better-app.git
git push -u origin main
```

### 2. Deploy with ArgoCD
```bash
# Apply ArgoCD application
kubectl apply -f argocd-app.yaml

# Or create via ArgoCD CLI
argocd app create better-app \
  --repo https://github.com/your-username/better-app \
  --path k8s/overlays/production \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace better-app \
  --sync-policy automated
```

### 3. Manual Deployment (Alternative)
```bash
# Deploy using kubectl
kubectl apply -k k8s/overlays/production
```

## Configuration

### Environment Variables
- `DB_PATH`: Database file path (default: `/data/names.db`)
- `FLASK_ENV`: Flask environment (production)

### Resource Limits
- **Requests**: 64Mi memory, 50m CPU
- **Limits**: 128Mi memory, 100m CPU (base), 256Mi/200m (production)

### Scaling
- **Base**: 3 replicas
- **Production**: 5 replicas
- **StatefulSet**: 1 replica (database)

## Monitoring

### Health Checks
- **Liveness**: `/health` endpoint
- **Readiness**: `/health` endpoint

### Probes Configuration
- Initial delay: 30s (liveness), 5s (readiness)
- Period: 10s (liveness), 5s (readiness)

## Storage
- **Type**: Persistent Volume Claims
- **Size**: 1Gi per StatefulSet replica
- **Access Mode**: ReadWriteOnce

## Security
- Non-root container user
- Resource limits enforced
- Network policies (recommended)
- TLS termination at ingress

## CI/CD Pipeline

### Triggers
- Push to `main` or `develop` branches
- Pull requests to `main`

### Stages
1. **Test**: Run pytest suite
2. **Build**: Create Docker image
3. **Push**: Push to GitHub Container Registry
4. **Deploy**: Update Kustomization with new image tag

### Secrets Required
- `GITHUB_TOKEN`: For container registry access

## Troubleshooting

### Common Issues
1. **Pod not starting**: Check resource limits and node capacity
2. **Database connection**: Verify StatefulSet and PVC status
3. **Ingress not working**: Check ingress controller and DNS

### Useful Commands
```bash
# Check application status
kubectl get pods -n better-app

# View logs
kubectl logs -f deployment/better-app -n better-app

# Check StatefulSet
kubectl get statefulset -n better-app

# View persistent volumes
kubectl get pv,pvc -n better-app

# ArgoCD sync status
argocd app get better-app
```

## Customization

### Adding Environment
1. Create new overlay in `k8s/overlays/staging`
2. Update ArgoCD application or create new one
3. Modify resource limits and replica counts as needed

### Database Migration
For production use, consider:
- PostgreSQL StatefulSet
- External managed database
- Database migration jobs

## Best Practices
- Use specific image tags in production
- Implement proper monitoring and alerting
- Regular backup of persistent data
- Network policies for security
- Resource quotas and limits
