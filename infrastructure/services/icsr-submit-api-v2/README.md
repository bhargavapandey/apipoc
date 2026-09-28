# ICSR Submit API v2 Service Definition

Service definition that assembles the ICSR Submit E2B Lambda function with infrastructure components.

## Overview

- **Application**: halopv
- **Domain**: icsr
- **Service**: submit-api
- **Version**: v2
- **Maintained by**: Development + DevOps

## Components

This service definition assembles:

1. **Lambda Function**: `halopv-icsr-submit-e2b-v2-lambda`
   - Source: `src/icsr-submit-e2b-v2/`
   - Layers: `halopv-requests-v2-layer`, `halopv-validation-v2-layer`

2. **API Gateway**: `halopv-icsr-api-v2`
   - Route: `POST /icsr/submit`
   - Integration: Lambda proxy

3. **IAM Role**: `halopv-icsr-submit-e2b-v2-role`
   - Permissions: CloudWatch Logs, DynamoDB (if configured)

## Deployment

See `infrastructure/environments/` for environment-specific configuration.

```bash
cd infrastructure/environments/dev
terraform apply
```
