# halopv-aws-api

AWS Lambda-based API repository following a source control, versioning, and release management best practices model.

## Repository Structure

This repository implements a unified source-of-truth approach for AWS Lambda applications, where:
- **Application source code** is maintained once and referenced/reused across services
- **Infrastructure definitions** are service-specific, not code-specific
- **Environment configuration** is separated from application logic
- **CI/CD pipelines** handle packaging and deployment automation

```
halopv-aws-api/
├── src/                          # Application source code (Lambda business logic)
├── layers/                        # Shared application libraries (Lambda layers)
├── infrastructure/
│   ├── modules/                   # Reusable Terraform modules (DevOps-managed)
│   ├── services/                  # Service definitions mapping app to infra
│   └── environments/              # Environment/deployment configuration
├── pipelines/                     # CI/CD pipeline definitions
├── docs/                          # Documentation
└── README.md
```

## Naming Conventions

Consistent vocabulary across the deployed chain:

| Component | Pattern | Example |
|-----------|---------|---------|
| Repository | `<app>-aws-api` | `halopv-aws-api` |
| Lambda source folder | `<domain>-<function>-<version>` | `icsr-submit-e2b-v2` |
| API Gateway | `<app>-<domain>-api-<ver>` | `halopv-icsr-api-v2` |
| Lambda function | `<app>-<domain>-<function>-<ver>-lambda` | `halopv-icsr-submit-e2b-v2-lambda` |
| Layer | `<app>-<purpose>-<ver>-layer` | `halopv-requests-v2-layer` |
| IAM role | `<app>-<domain>-<function>-<ver>-role` | `halopv-icsr-submit-e2b-v2-role` |

## Key Principles

1. **Single Source of Truth for Code**: Each Lambda function exists once in Git
2. **Reusable Definitions**: Service definitions assemble modules and reference application code
3. **Version in Source Tree**: Versioning is part of the branch/folder structure
4. **Environment Separation**: Environment-specific config is in `infrastructure/environments/`, not embedded in source
5. **Generated Artifacts Outside Git**: Lambda deployment packages and Terraform state belong in S3 and remote backends
6. **Ownership Model**: 
   - **Development**: Maintains `src/` and `layers/`
   - **DevOps**: Maintains `infrastructure/modules/`, `infrastructure/environments/`, and `pipelines/`
   - **Shared**: `infrastructure/services/` (Development + DevOps)

## Getting Started

See individual subdirectory READMEs for detailed guidance on each component.
