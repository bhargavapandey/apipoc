# Documentation

## Repository Structure

This AWS Lambda repository demonstrates a scalable, source-controlled approach to managing Lambda functions, layers, infrastructure, and deployments.

### Directory Organization

#### `src/` - Application Source Code

Lambda business logic maintained by Development teams:

- `icsr-submit-e2b-v2/` - ICSR submission handler
- `mhra-export-data-v1/` - MHRA data export functionality

Each service folder contains:
- `lambda_function.py` - Main handler
- `requirements.txt` - Python dependencies
- `tests/` - Unit tests
- `README.md` - Service documentation

#### `layers/` - Shared Lambda Layers

Reusable code libraries and utilities:

- `halopv-requests-v2-layer/` - HTTP utilities with retry logic
- `halopv-mhra-format-v1-layer/` - MHRA format conversion
- `halopv-validation-v2-layer/` - Data validation utilities

Layers reduce code duplication and improve consistency across services.

#### `infrastructure/`

**modules/** - Reusable Terraform modules (DevOps-managed):
- `lambda/` - Lambda function deployment
- `api_gateway/` - API Gateway integration

**services/** - Service definitions (Development + DevOps):
- `icsr-submit-api-v2/` - ICSR submission service
- `mhra-export-api-v1/` - MHRA export service

Services assemble modules and reference application code.

**environments/** - Environment-specific configuration (DevOps-managed):
- `dev/` - Development environment
- `staging/` - Staging environment
- `prod/` - Production environment

Each environment has:
- `main.tf` - Environment-specific resource definitions
- `terraform.tfvars` - Environment configuration values
- `variables.tf` - Variable definitions
- `outputs.tf` - Output definitions

#### `pipelines/` - CI/CD Pipelines (DevOps-managed)

- `github-actions/deploy.yml` - Multi-stage deployment workflow

Pipeline stages:
1. **Build** - Tests and packages Lambda functions
2. **Deploy Dev** - Automatic deployment to dev on develop branch
3. **Deploy Staging** - Automatic deployment to staging on main branch
4. **Deploy Prod** - Manual deployment to production with approval

## Key Principles

### 1. Single Source of Truth

Each Lambda function exists once in the repository:
- Located in `src/<domain>-<function>-<version>/`
- Referenced by service definitions
- Never duplicated for customer/endpoint/environment

### 2. Versioning in Source Tree

Versions are part of the folder structure:
- Source: `src/icsr-submit-e2b-v2/`
- Allows multiple versions to coexist
- Can branch by version when needed

### 3. Environment Separation

Environment-specific configuration is isolated:
- Deployment targets: `infrastructure/environments/`
- Environment variables injected by Terraform
- No environment-specific code in application source

### 4. Infrastructure as Code

All AWS resources defined in Terraform:
- Lambda functions
- API Gateways
- IAM roles and policies
- S3 buckets
- CloudWatch monitoring

### 5. Naming Conventions

Consistent vocabulary across the deployed chain:

| Component | Pattern | Example |
|-----------|---------|----------|
| Repository | `<app>-aws-api` | halopv-aws-api |
| Lambda source | `<domain>-<function>-<version>` | icsr-submit-e2b-v2 |
| API Gateway | `<app>-<domain>-api-<ver>` | halopv-icsr-api-v2 |
| Lambda function | `<app>-<domain>-<function>-<ver>-lambda` | halopv-icsr-submit-e2b-v2-lambda |
| Layer | `<app>-<purpose>-<ver>-layer` | halopv-requests-v2-layer |
| IAM role | `<app>-<domain>-<function>-<ver>-role` | halopv-icsr-submit-e2b-v2-role |

### 6. Ownership Model

- **Development**: Maintains `src/` and `layers/`
- **DevOps**: Maintains `infrastructure/modules/`, `infrastructure/environments/`, `pipelines/`
- **Shared**: `infrastructure/services/` (coordinates between Dev and DevOps)

## Deployment Flow

### Development Push

```
Developer → Git commit → GitHub
                ↓
         GitHub Actions Workflow
            (pipeline/github-actions/deploy.yml)
                ↓
         ┌─────────────────┬─────────────────┬─────────────────┐
         │      BUILD      │    DEPLOY DEV   │  DEPLOY STAGING │
         └─────────────────┴─────────────────┴─────────────────┘
                                      ↓
                             AWS CloudFormation
                             (Terraform Apply)
                                      ↓
                             Lambda + API Gateway
```

### Branching Strategy

- **develop** → Dev environment (automatic)
- **main** → Staging (automatic) + Production (manual approval)

## Adding a New Service

### Step 1: Create Source Code

```
src/
└── <domain>-<function>-<version>/
    ├── lambda_function.py
    ├── requirements.txt
    ├── README.md
    └── tests/
```

### Step 2: Create Service Definition

```
infrastructure/services/
└── <domain>-<function>-api-<version>/
    ├── main.tf       # Service assembly
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

### Step 3: Deploy to Environments

Reference the service in each environment:

```hcl
module "my_service" {
  source = "../../services/<domain>-<function>-api-<version>"
  environment = var.environment
  ...
}
```

### Step 4: Update Pipelines

Add build/deploy steps for the new service in `pipelines/github-actions/deploy.yml`.

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- Python 3.11+
- GitHub Actions secrets configured (AWS role ARNs)

### Local Development

```bash
# Test Lambda locally
cd src/<service-name>
pip install -r requirements.txt
python -m pytest tests/

# Deploy infrastructure
cd infrastructure/environments/dev
terraform init
terraform plan
terraform apply
```

### Infrastructure Deployment

```bash
# Dev environment
cd infrastructure/environments/dev
terraform apply -var="lambda_package_path=../../../build/function.zip"

# Staging environment
cd infrastructure/environments/staging
terraform apply -var="lambda_package_path=../../../build/function.zip"

# Production environment
cd infrastructure/environments/prod
terraform apply -var="lambda_package_path=../../../build/function.zip"
```

## References

- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
