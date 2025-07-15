# Better App

A simple Flask web application for managing a list of names.

## Features
- Add names to a list
- Edit existing names
- Delete names from the list
- Clean, modern UI with responsive design

## Development Environment

This project is configured for development environment only.

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Using the development script
```bash
./run-dev.sh
```

#### Option 2: Manual setup
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
export LOG_LEVEL=DEBUG
python app.py
```

The application will be available at `http://localhost:5000`

### Development Features
- Debug mode enabled
- Detailed logging
- Local SQLite database (`dev_names.db`)
- Hot reloading for code changes

## Kubernetes Deployment

The application is configured for deployment to a Kubernetes development environment:

```bash
# Apply the ArgoCD application
kubectl apply -f argocd-app.yaml

# Or deploy directly with Kustomize
kubectl apply -k k8s/overlays/dev
```

## Usage
- Enter a name in the input field and click "Add Name"
- Click "Edit" next to any name to modify it
- Click "Delete" to remove a name from the list
