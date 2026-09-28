# Quick Start Guide

## Repository Overview

**halopv-aws-api** is a monorepo containing AWS Lambda functions, shared libraries (layers), Terraform infrastructure, and CI/CD pipelines for the HaloPV healthcare application.

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.5
- Python 3.11+
- Git
- GitHub CLI (optional but recommended)

### 1. Clone Repository

```bash
git clone https://github.com/your-org/halopv-aws-api.git
cd halopv-aws-api
```

### 2. Set Up Local Environment

```bash
# Install Python dependencies
cd src/icsr-submit-e2b-v2
pip install -r requirements.txt
pip install pytest pytest-cov

# Install AWS SAM CLI (for local testing)
brew install aws-sam-cli
```

### 3. Run Tests Locally

```bash
# Test ICSR service
cd src/icsr-submit-e2b-v2
python -m pytest tests/ -v --cov=.

# Test MHRA service
cd ../mhra-export-data-v1
python -m pytest tests/ -v --cov=.
```

### 4. Create a Feature Branch

```bash
# Pull latest develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/my-feature

# Make your changes
git add .
git commit -m "feat: Add new feature description"

# Push and create PR
git push origin feature/my-feature
```

### 5. Deploy to Dev Environment

```bash
# Terraform automatically deploys on merge to develop
# Or manually trigger:

cd infrastructure/environments/dev
terraform init
terraform plan -var="lambda_package_path=../../../build/icsr-submit-e2b-v2.zip"
terraform apply
```

## File Structure Quick Reference

```
halopv-aws-api/
│
├── src/                                # Lambda functions (Development-owned)
│   ├── icsr-submit-e2b-v2/
│   │   ├── lambda_function.py         # Main handler
│   │   ├── requirements.txt           # Dependencies
│   │   └── tests/                     # Unit tests
│   │
│   └── mhra-export-data-v1/
│       ├── lambda_function.py
│       ├── requirements.txt
│       └── tests/
│
├── layers/                             # Lambda layers (Development-owned)
│   ├── halopv-requests-v2-layer/      # HTTP utilities
│   ├── halopv-mhra-format-v1-layer/   # MHRA conversion
│   └── halopv-validation-v2-layer/    # Validation utilities
│
├── infrastructure/                     # IaC & Deployment (DevOps-owned)
│   │
│   ├── modules/                       # Reusable Terraform modules
│   │   ├── lambda/                    # Lambda deployment
│   │   └── api_gateway/               # API Gateway
│   │
│   ├── services/                      # Service definitions (Dev + DevOps)
│   │   ├── icsr-submit-api-v2/
│   │   └── mhra-export-api-v1/
│   │
│   └── environments/                  # Environment configs (DevOps-owned)
│       ├── dev/
│       ├── staging/
│       └── prod/
│
├── pipelines/                          # CI/CD workflows (DevOps-owned)
│   └── github-actions/
│       └── deploy.yml                 # Main pipeline
│
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md                # Overall design
│   ├── BRANCHING_STRATEGY.md          # Git workflow
│   └── MONOREPO_VS_MULTIREPO.md       # Design decisions
│
└── README.md                           # Main readme
```

## Common Tasks

### Add a New Lambda Function

1. Create source directory
```bash
mkdir -p src/<domain>-<function>-v<version>
cd src/<domain>-<function>-v<version>
```

2. Create files
```bash
touch lambda_function.py requirements.txt README.md
mkdir tests
```

3. Create service definition
```bash
mkdir -p infrastructure/services/<domain>-<function>-api-v<version>
# Copy from existing service and modify
```

4. Add to pipeline
```yaml
# pipelines/github-actions/deploy.yml
- name: Package new function
  run: |
    cd src/<domain>-<function>-v<version>
    zip -r ../../build/<domain>-<function>-v<version>.zip .
```

### Add a New Lambda Layer

1. Create layer directory
```bash
mkdir -p layers/halopv-<purpose>-v<version>/python
```

2. Add code
```bash
touch layers/halopv-<purpose>-v<version>/python/module.py
touch layers/halopv-<purpose>-v<version>/python/__init__.py
```

3. Update services to use layer
```hcl
layer_arns = [
  "arn:aws:lambda:${region}:${account}:layer:halopv-<purpose>-v<version>:1"
]
```

### Deploy Service to Different Environment

```bash
# Dev (auto on develop branch)
git checkout develop
git pull
# Tests run, deployments happen automatically

# Staging (auto on main branch)
git checkout main
git pull
# Tests run, deployments happen automatically

# Production (manual, requires approval)
gh workflow run deploy.yml -f environment=prod
```

### Check Deployment Status

```bash
# View recent deployments
gh workflow view deploy.yml

# View specific deployment logs
gh run view <run-id> -w deploy.yml
```

### Rollback Deployment

```bash
# Redeploy previous version
gh workflow run deploy.yml \
  -f environment=prod \
  -f version=v2.0.5
```

## Useful Commands

```bash
# View all branches
git branch -a

# View commit history
git log --oneline --graph --all

# See what changed
git diff develop...main

# Create a release
git flow release start v2.1.0
git flow release finish v2.1.0

# View tags
git tag -l --sort=-version:refname
```

## Troubleshooting

### Test Failures

```bash
# Run tests with verbose output
pytest -vvv --tb=short

# Run specific test
pytest tests/test_lambda_function.py::test_lambda_handler_success -v
```

### Terraform Errors

```bash
# Validate Terraform
terraform validate

# Check what will change
terraform plan -out=tfplan

# Format Terraform files
terraform fmt -recursive
```

### Deployment Failures

```bash
# Check Lambda logs
aws logs tail /aws/lambda/halopv-icsr-submit-e2b-v2-lambda --follow

# Check API Gateway errors
aws apigatewayv2 get-apis
```

## Key Documentation Files

- **ARCHITECTURE.md** - Overall design and structure
- **BRANCHING_STRATEGY.md** - Git branching and versioning
- **MONOREPO_VS_MULTIREPO.md** - Design decision rationale
- **README.md** - Main repository information

## Getting Help

- Check relevant README.md in each service directory
- Review ARCHITECTURE.md for design questions
- Look at existing PRs for examples
- Check CI/CD logs for deployment issues

## Next Steps

1. ✅ Clone repository and run tests locally
2. ✅ Read ARCHITECTURE.md to understand design
3. ✅ Review BRANCHING_STRATEGY.md for Git workflow
4. ✅ Create feature branch and make first change
5. ✅ Submit PR and have it reviewed
6. ✅ Watch automated deployment to dev environment
