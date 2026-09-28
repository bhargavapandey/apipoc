# Recommended Repository Layout and Branch Policy

**Status:** Proposed
**Repository:** `bhargavapandey/apipoc`
**Decision:** Use one repository per application, with multiple logical services inside the repository.

## 1. Recommendation

For the current AWS Lambda model, `halopv-aws-api` should be managed as an application monorepo:

- Keep each Lambda application source in `src/` exactly once.
- Keep reusable Lambda layers in `layers/`.
- Keep reusable Terraform building blocks in `infrastructure/modules/`.
- Keep service-to-infrastructure assembly in `infrastructure/services/`.
- Keep deployment-specific values in `infrastructure/environments/`.
- Keep build, test, packaging, and deployment workflows in `pipelines/`.
- Store generated ZIP files, Terraform state, and runtime artifacts outside Git.

This provides a single source of truth while allowing each service to remain independently testable and deployable.

## 2. Recommended Repository Layout

```text
halopv-aws-api/
├── src/                                  # Development-owned application code
│   ├── icsr-submit-e2b-v2/               # Lambda business logic
│   │   ├── lambda_function.py
│   │   ├── requirements.txt
│   │   ├── tests/
│   │   └── README.md
│   └── mhra-export-data-v1/               # Additional Lambda service
│       ├── lambda_function.py
│       ├── requirements.txt
│       ├── tests/
│       └── README.md
│
├── layers/                               # Development-owned reusable layers
│   ├── halopv-requests-v2-layer/
│   │   ├── python/
│   │   └── README.md
│   ├── halopv-validation-v2-layer/
│   │   ├── python/
│   │   └── README.md
│   └── halopv-mhra-format-v1-layer/
│       ├── python/
│       └── README.md
│
├── infrastructure/
│   ├── modules/                          # DevOps-owned reusable Terraform modules
│   │   ├── lambda/
│   │   └── api_gateway/
│   ├── services/                         # Shared Development + DevOps ownership
│   │   ├── icsr-submit-api-v2/
│   │   └── mhra-export-api-v1/
│   └── environments/                     # DevOps-owned deployment configuration
│       ├── dev/
│       ├── staging/
│       └── prod/
│
├── pipelines/                            # DevOps-owned CI/CD
│   └── github-actions/
│       └── deploy.yml
│
├── docs/                                 # Architecture and operating guidance
│   ├── ARCHITECTURE.md
│   ├── BRANCHING_STRATEGY.md
│   ├── MONOREPO_VS_MULTIREPO.md
│   └── QUICKSTART.md
│
├── .github/
│   ├── CODEOWNERS
│   └── pull_request_template.md
└── README.md
```

## 3. Ownership Boundaries

| Area | Primary owner | Responsibility |
|---|---|---|
| `src/` | Development | Lambda business logic, tests, and application dependencies |
| `layers/` | Development | Reusable libraries, schemas, and layer dependencies |
| `infrastructure/modules/` | DevOps | Reusable Terraform building blocks |
| `infrastructure/services/` | Development + DevOps | Mapping application code to AWS infrastructure |
| `infrastructure/environments/` | DevOps | Environment values, state backends, and deployment targets |
| `pipelines/` | DevOps | Build, test, package, plan, apply, and release automation |
| `docs/` | Shared | Architecture, standards, and operating procedures |

## 4. Branch Policy

Use a protected-branch workflow with short-lived feature branches.

```text
main       ─────────────── production
  ▲
release/*  ─────────────── release stabilization
  ▲
staging    ─────────────── UAT and pre-production
  ▲
develop    ─────────────── integration and dev deployment
  ▲
feature/* / bugfix/*
```

### Protected branches

#### `main`

- Represents production-ready code.
- Deploys to production after merge and approval.
- Requires at least two reviewers for infrastructure or production-impacting changes.
- Requires all mandatory CI checks to pass.
- Disallows direct commits, force pushes, and branch deletion.
- Receives changes from approved `release/*` or `hotfix/*` pull requests only.
- Every production release must have an immutable Git tag.

#### `staging`

- Represents the release candidate deployed to staging.
- Used for integration testing and UAT.
- Requires at least one reviewer and successful CI checks.
- Receives changes from `develop` or a release branch.
- Direct commits and force pushes are prohibited.

#### `develop`

- Integration branch for completed features.
- Deploys automatically to the development environment.
- Requires at least one reviewer and successful CI checks.
- Receives changes through pull requests from short-lived branches.

### Short-lived branches

Use the following naming conventions:

```text
feature/<issue>-<description>
bugfix/<issue>-<description>
hotfix/<version>-<description>
release/<version>
```

Examples:

```text
feature/123-add-mhra-json-export
bugfix/456-handle-invalid-e2b-date
release/v2.1.0
hotfix/v2.1.1-api-timeout
```

Branch rules:

- Create `feature/*` and `bugfix/*` from `develop`.
- Create `release/*` from `staging` after the release scope is agreed.
- Create `hotfix/*` from `main` for urgent production corrections.
- Keep branches short-lived and rebase or merge from the target branch before review.
- Delete merged branches.

## 5. Versioning and Releases

Use Semantic Versioning for deployable components:

```text
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking API, schema, or compatibility change.
- **MINOR**: Backward-compatible feature.
- **PATCH**: Backward-compatible bug or security fix.

The source-tree version identifies the API or compatibility generation:

```text
src/icsr-submit-e2b-v2/
src/mhra-export-data-v1/
infrastructure/services/icsr-submit-api-v2/
```

Git release tags identify the deployed release:

```text
v2.1.0
v2.1.0-rc.1
v2.1.0-dev.5
```

For independent service releases, optional service-scoped tags may be used:

```text
icsr-submit-e2b/v2.1.0
mhra-export-data/v1.1.0
```

### Release flow

1. Merge completed work into `develop`.
2. Promote the tested commit to `staging`.
3. Create `release/vX.Y.Z` from `staging`.
4. Run full integration, security, and UAT validation.
5. Merge the release branch into `main` through an approved pull request.
6. Create and push the immutable `vX.Y.Z` tag.
7. Deploy the tagged release to production.
8. Merge production fixes back into `develop` and `staging` where required.

### Hotfix flow

1. Create `hotfix/vX.Y.Z` from `main`.
2. Apply the smallest safe correction and run targeted tests.
3. Merge into `main` after emergency review.
4. Tag and deploy the patch release.
5. Merge the hotfix back into `staging` and `develop`.

## 6. CI/CD Expectations

Every pull request should run, as applicable:

- Unit tests for changed services and layers.
- Formatting and lint checks.
- Terraform formatting and validation.
- Security and dependency scanning.
- Packaging validation.
- Terraform plan for affected environments.

Deployment behavior:

| Source | Target | Policy |
|---|---|---|
| `develop` | Dev | Automatic after merge |
| `staging` or `release/*` | Staging | Automatic or approval-gated |
| `main` and release tag | Production | Approval-gated |

Use path-based change detection so an unrelated service does not needlessly rebuild or deploy. Shared layer and Terraform module changes should trigger all dependent service validation.

## 7. Monorepo Decision and Future Split Criteria

The application monorepo is the preferred model now because services share:

- Lambda layers and dependency definitions.
- Terraform modules and service conventions.
- Security, monitoring, and release controls.
- Cross-service schema and API changes.

Do not split into multiple repositories solely because there are multiple Lambda functions.

Reconsider a multi-repository model when most of the following are true:

- There are approximately 10 or more independently operated services.
- Services are owned by autonomous teams with separate release cadences.
- Services have minimal shared source and infrastructure.
- Independent access controls or compliance boundaries are required.
- Teams can publish and consume versioned shared layers reliably.

If a split becomes necessary, keep a small platform or infrastructure repository for shared modules and deployment standards, and publish shared layers as versioned artifacts rather than copying source code.

## 8. Decision

Adopt **one repository per application with multiple services inside it**, using protected `main`, `staging`, and `develop` branches, short-lived feature branches, Semantic Versioning, and immutable release tags.

This is the simplest and safest approach for the current service count while preserving a clear path to multi-repository ownership if the application and teams grow significantly.
