#!/bin/bash

# Simple deployment script for Better App

echo "Better App Kubernetes Deployment"
echo "================================="

# Create namespace
echo "Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Apply services
echo "Applying services..."
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/headless-service.yaml

# Choose deployment type
echo ""
echo "Choose deployment type:"
echo "1) StatefulSet (with persistent storage)"
echo "2) Deployment (stateless with rolling updates)"
echo "3) Both (for testing)"

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Deploying StatefulSet..."
        kubectl apply -f k8s/statefulset.yaml
        kubectl get statefulset -n better-app-dev
        ;;
    2)
        echo "Deploying Deployment..."
        kubectl apply -f k8s/deployment.yaml
        kubectl get deployment -n better-app-dev
        ;;
    3)
        echo "Deploying both StatefulSet and Deployment..."
        kubectl apply -f k8s/statefulset.yaml
        kubectl apply -f k8s/deployment.yaml
        kubectl get all -n better-app-dev
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "Deployment complete!"
echo "Check status with: kubectl get pods -n better-app-dev"
echo "View logs with: kubectl logs -f -n better-app-dev -l app=better-app"
