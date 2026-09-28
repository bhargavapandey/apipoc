# CI/CD Pipelines

This directory contains CI/CD pipeline definitions for building, testing, and deploying services.

## GitHub Actions

### deploy.yml

Main deployment pipeline that:

1. **Build Stage**
   - Checkout code
   - Run unit tests
   - Package Lambda function
   - Upload artifacts

2. **Deploy Dev**
   - Triggered on push to `develop` branch
   - Deploys to dev environment
   - Runs smoke tests

3. **Deploy Staging**
   - Triggered on push to `main` branch
   - Deploys to staging environment
   - Runs integration tests

4. **Deploy Production**
   - Triggered on push to `main` branch (requires approval)
   - Deploys to production environment
   - Requires production environment approval

## Secrets Required

The following secrets must be configured in GitHub:

- `AWS_ROLE_DEV`: IAM role ARN for dev deployments
- `AWS_ROLE_STAGING`: IAM role ARN for staging deployments
- `AWS_ROLE_PROD`: IAM role ARN for production deployments

## Branching Strategy

- **develop**: Dev environment deployments
- **main**: Staging and production deployments

## Running Deployments

### Automatic

Push to develop or main branch with changes in:
- `src/`
- `layers/`
- `infrastructure/`
- `pipelines/`

### Manual

Use workflow dispatch to manually trigger deployments:

```bash
gh workflow run deploy.yml -f environment=dev
```
