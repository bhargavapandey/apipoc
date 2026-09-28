# One Repository vs. Multiple Repositories

## Executive Summary

**Recommendation: Monorepo (One Repository) for halopv-aws-api**

For the HaloPV AWS Lambda ecosystem, a **single repository with multiple services** is the better choice because:

- ✅ Shared dependency management (layers)
- ✅ Coordinated releases and versioning
- ✅ Unified CI/CD pipeline
- ✅ Simplified infrastructure management
- ✅ Easier cross-service changes
- ✅ Single source of truth for IaC

However, future growth may warrant transitioning to **multi-repo with careful coordination**.

---

## Monorepo: One Repository (`halopv-aws-api`)

### Structure

```
halopv-aws-api/
├── src/
│   ├── icsr-submit-e2b-v2/
│   ├── mhra-export-data-v1/
│   └── medical-review-v1/
├── layers/
│   ├── halopv-requests-v2-layer/
│   ├── halopv-mhra-format-v1-layer/
│   └── halopv-validation-v2-layer/
├── infrastructure/
│   ├── modules/
│   ├── services/
│   └── environments/
└── pipelines/
```

### ✅ Advantages

#### 1. **Shared Code & Dependencies**

```
Layers are single source of truth:
- requests-v2-layer is used by multiple services
- No duplication or version conflicts
- Update once, used everywhere
```

**Benefit**: Consistency, reduced maintenance

#### 2. **Atomic Transactions Across Services**

```bash
# Change that affects multiple services
# Example: Update validation layer API

One commit contains:
├── layers/halopv-validation-v2-layer/   (update)
├── src/icsr-submit-e2b-v2/             (update imports)
├── src/mhra-export-data-v1/            (update imports)
└── tests/                               (add test coverage)

# Single PR, single deployment, all tested together
```

**Benefit**: Prevents breaking changes across services

#### 3. **Unified Versioning & Release**

```
v2.1.0 release includes:
├── ICSR Submit E2B v2.1.0
├── MHRA Export v1.1.0
├── Requests Layer v2.0.0
└── All coordinated in one tag

No confusion about compatibility
```

**Benefit**: Clear release management, no integration headaches

#### 4. **Simplified CI/CD**

```yaml
# Single pipeline handles everything
name: Deploy HaloPV API
on:
  push:
    branches: [main, staging, develop]
  
jobs:
  build:
    # Test all services in one job
    # Package all layers
    # Generate all artifacts
  
  deploy-dev:
    # Deploy all services to dev in one job
  
  deploy-staging:
    # Deploy all services to staging
  
  deploy-prod:
    # Deploy all services to prod
```

**Benefit**: Single pipeline, easier maintenance, fewer secrets/vars

#### 5. **Unified Infrastructure**

```hcl
# All services in one Terraform state
infrastructure/environments/prod/terraform.tfstate
├── ICSR Submit API
├── MHRA Export API
├── API Gateway routing
└── Shared resources (CloudWatch, S3)

# Cross-service infrastructure changes easy to test together
```

**Benefit**: Prevents infrastructure drift, coordinated changes

#### 6. **Easier Cross-Service Changes**

```python
# Scenario: Add new field to submission schema
# Affects: validation layer, ICSR service, MHRA export service

# Single PR across all:
1. Update e2b_schema.py in validation layer
2. Update lambda_function.py in ICSR service
3. Update mhra_format.py in export service
4. Update tests in all services
5. Single CI run validates everything
```

**Benefit**: No coordination between repos, no version mismatches

#### 7. **Code Reuse & Standards**

```
Shared utilities always at latest:
├── Layer updates applied immediately
├── Request patterns consistent
├── Error handling standardized
└── All services follow same conventions
```

**Benefit**: Better consistency, easier onboarding

#### 8. **Bisect & Blame Across Services**

```bash
# Track down what broke submission processing
git bisect start
# Finds the exact commit (could be layer change or service change)

# See who changed what across all services
git log --all --grep="validation" -- .
```

**Benefit**: Easier debugging, better traceability

### ❌ Disadvantages

#### 1. **Larger Repository Size**

```bash
# As services grow
git clone halopv-aws-api  # Slower
git log                   # More history to traverse
```

**Mitigation**: Use shallow clones, monorepo tools (Nx, Lerna)

#### 2. **Fewer Access Controls**

```bash
# Can't restrict: "only MHRA team can merge MHRA code"
# All developers have access to all services
```

**Mitigation**: Code review practices, CODEOWNERS file

#### 3. **Coupling Risk**

```
If not careful:
├── Changes to layer break multiple services
├── Circular dependencies form
└── Monorepo becomes a "big ball of mud"
```

**Mitigation**: Clear module boundaries, enforce layer usage patterns

#### 4. **Testing Complexity**

```bash
# Must test all services together
# Even if only one service changed

pytest tests/          # Runs all tests
# Takes longer than testing single service
```

**Mitigation**: Parallelized testing, CI optimization

#### 5. **Slower Development for Unrelated Teams**

```
Team A working on ICSR
Team B working on MHRA

# Both affected by same main repo status
# Merge conflicts possible
# CI pipeline blocks both teams
```

**Mitigation**: Strong CI/CD, good PR practices, parallelized jobs

---

## Multi-Repo: Separate Repository Per Service

### Structure

```
halopv-aws-api/              (infrastructure + orchestration)
halopv-icsr-submit-e2b/      (service repo)
halopv-mhra-export-data/     (service repo)
halopv-lambda-layers/        (shared layers repo)
```

### ✅ Advantages

#### 1. **Independent Deployment**

```bash
# Deploy MHRA v1.2.0 without touching ICSR
# ICSR stays at v2.1.0

halopv-mhra-export-data/ → CI/CD → Deploy
```

**Benefit**: Faster deployments, independent release cycles

#### 2. **Clearer Ownership**

```bash
# MHRA Team owns halopv-mhra-export-data/
# ICSR Team owns halopv-icsr-submit-e2b/

# Easy to enforce access control at repo level
```

**Benefit**: Clear team boundaries, easier permission management

#### 3. **Smaller Repositories**

```bash
git clone halopv-mhra-export-data/  # Small, fast
git log                              # Relevant history only
```

**Benefit**: Faster operations, easier to search

#### 4. **Less Coupling**

```python
# ICSR repo can make changes
# Without affecting MHRA repo

# Loose coupling is better for scaling
```

**Benefit**: Teams can move faster independently

#### 5. **Independent Testing**

```bash
halopv-icsr-submit-e2b/pytest  # Only ICSR tests
halopv-mhra-export-data/pytest # Only MHRA tests

# Can run in parallel without interference
```

**Benefit**: Faster CI/CD for individual services

### ❌ Disadvantages

#### 1. **Shared Dependency Management Complexity**

```
halopv-lambda-layers/ (version 2.1.0)
    ├── Used by halopv-icsr-submit-e2b/
    ├── Used by halopv-mhra-export-data/
    └── Used by halopv-medical-review/

What if layer updates break ICSR?
- ICSR repo needs to be tested
- But change is in different repo
- Who coordinates the test?
```

**Challenge**: Version coordination nightmare

#### 2. **Coordinated Deployments Are Painful**

```bash
# Need to deploy validation-layer v2.1.0
# Which requires updating all service repos

1. Update halopv-lambda-layers/ → v2.1.0
2. Update halopv-icsr-submit-e2b/ → use v2.1.0
3. Update halopv-mhra-export-data/ → use v2.1.0
4. Test all three repos together
5. Deploy in correct order

# 3+ PRs, 3+ deployments, manual coordination
```

**Challenge**: Complex release management

#### 3. **Breaking Changes Across Repos**

```python
# Validation layer changes API
# halopv-lambda-layers/ v3.0.0

# All service repos must update simultaneously
# Or compatibility breaks

# What if ICSR updates but MHRA doesn't?
# They have different versions of same layer
```

**Challenge**: Version mismatches, integration issues

#### 4. **Infrastructure Duplication**

```hcl
# Terraform code for ICSR
infrastructure/icsr/main.tf
├── API Gateway setup
├── Lambda configuration
├── IAM roles
└── Monitoring

# Same code copied for MHRA
infrastructure/mhra/main.tf
├── API Gateway setup (duplicated)
├── Lambda configuration (duplicated)
├── IAM roles (duplicated)
└── Monitoring (duplicated)

# Update in one place, need to update in both
```

**Challenge**: Maintenance burden, DRY violation

#### 5. **Atomic Transactions Impossible**

```bash
# Fix that requires changing validation layer + ICSR + MHRA
# Needs 3 separate PRs, 3 separate merges
# Can't guarantee all are deployed together

# Period where code is inconsistent
```

**Challenge**: Increased risk of broken states

#### 6. **Multiple CI/CD Pipelines**

```yaml
# halopv-lambda-layers/.github/workflows/deploy.yml
# halopv-icsr-submit-e2b/.github/workflows/deploy.yml
# halopv-mhra-export-data/.github/workflows/deploy.yml
# halopv-aws-api/.github/workflows/orchestrate.yml

# 4 separate pipelines to maintain
# Different configurations, secrets, variables
# Hard to keep in sync
```

**Challenge**: Pipeline maintenance burden

#### 7. **Difficult Cross-Service Changes**

```python
# Need to add field to E2B schema
# Affects validation + ICSR + MHRA + documentation

# Solution with multi-repo:
1. Create issue linking all 4 repos
2. Create branch in halopv-lambda-layers/
3. Create branch in halopv-icsr-submit-e2b/
4. Create branch in halopv-mhra-export-data/
5. Create branch in halopv-aws-api/
6. Create 4 separate PRs
7. Coordinate 4 reviews
8. Merge all together (timing is critical)
9. Deploy in order

# Much more complex than monorepo approach
```

**Challenge**: Coordination overhead, more error-prone

---

## Comparison Matrix

| Aspect | Monorepo (One Repo) | Multi-Repo (Multiple Repos) |
|--------|--------------------|-----------|
| **Shared Dependencies** | ✅ Easy management | ❌ Version coordination required |
| **Release Coordination** | ✅ Single tag | ❌ Multiple tags, ordering matters |
| **Atomic Transactions** | ✅ Supported | ❌ Difficult/impossible |
| **Deployment Speed** | ⚠️ Slower (test all) | ✅ Faster (per-service) |
| **Repo Size** | ⚠️ Larger | ✅ Smaller |
| **Team Independence** | ⚠️ Limited | ✅ High |
| **CI/CD Complexity** | ✅ Single pipeline | ⚠️ Multiple pipelines |
| **Code Reuse** | ✅ Straightforward | ⚠️ Requires publishing |
| **Access Control** | ⚠️ Repository-wide | ✅ Per-repo easy |
| **Onboarding** | ✅ Clone once | ❌ Clone multiple repos |
| **Debugging** | ✅ Single source | ⚠️ Requires searching multiple |
| **Scalability** | ⚠️ Best to ~10 services | ✅ Scales to 100+ services |

---

## Recommendation: Monorepo NOW, Multi-Repo LATER

### Phase 1: Current State (Monorepo)
**Services**: 2-3 core services

```
halopv-aws-api/  (single repo)
├── src/
│   ├── icsr-submit-e2b-v2/
│   └── mhra-export-data-v1/
├── layers/
└── infrastructure/
```

**Why**: Easier to manage shared code, coordinated releases, simpler CI/CD

### Phase 2: Growth (Monorepo with Workspaces)
**Services**: 5-10 services

```
halopv-aws-api/  (monorepo with workspaces)
├── packages/
│   ├── icsr-submit-e2b-v2/
│   ├── mhra-export-data-v1/
│   ├── medical-review-v1/
│   ├── adverse-event-v1/
│   └── reporting-v1/
├── layers/
└── infrastructure/
```

**Tools**: Use Nx or Lerna for workspace management

### Phase 3: Scaling (Multi-Repo)
**Services**: 10+ services, independent teams

```
halopv-aws-api/              (orchestration + shared infra)
halopv-icsr-submit-e2b/      (team-owned repo)
halopv-mhra-export-data/     (team-owned repo)
halopv-medical-review/       (team-owned repo)
halopv-lambda-layers/        (shared utilities)
```

**Implementation**:
- Publish layers to Lambda Layer repository
- Versioned dependencies in each service
- Separate CI/CD per service
- Orchestration layer for coordinated deployments

---

## Decision Flow

```
┌─ How many services?
├─ 1-2 services?
│  └─ Monorepo (simplest)
│
├─ 3-5 services with shared code?
│  └─ Monorepo with clear module boundaries
│
├─ 5-10 services, some shared, some independent?
│  └─ Monorepo with workspaces (Nx/Lerna)
│
└─ 10+ services, multiple independent teams?
   └─ Multi-repo with shared layer registry
```

---

## Implementation Guide for Monorepo

### Best Practices

1. **Clear Module Boundaries**
   ```
   src/<domain>-<function>/  # Clear ownership
   Each service is self-contained
   Layers are utilities only, not business logic
   ```

2. **Enforce Dependency Rules**
   ```python
   # ✅ ICSR can use layers
   from requests_utils import Session
   
   # ❌ ICSR should NOT use MHRA-specific code
   from mhra_format import convert_to_csv  # Wrong!
   ```

3. **Independent Testing**
   ```bash
   pytest src/icsr-submit-e2b-v2/tests/     # Test one service
   pytest src/mhra-export-data-v1/tests/    # Test another
   pytest layers/                             # Test layers
   pytest                                     # All tests (CI)
   ```

4. **Coordinated Release**
   ```
   - All services must be compatible with shared layers
   - Version bump in layer may require service updates
   - Tag coordinated releases together
   ```

5. **Clear CODEOWNERS**
   ```
   # .github/CODEOWNERS
   src/icsr-submit-e2b-v2/        @icsr-team
   src/mhra-export-data-v1/       @mhra-team
   layers/                         @platform-team
   infrastructure/                 @devops-team
   ```

---

## Conclusion

**For halopv-aws-api, the monorepo approach is recommended** because:

1. ✅ Shared Lambda layers need coordination
2. ✅ Services share common patterns (validation, requests)
3. ✅ Infrastructure is unified (API Gateway, IAM)
4. ✅ Currently 2-3 services (not at scale yet)
5. ✅ Simpler CI/CD and releases
6. ✅ Easier to maintain consistency

**However, keep this in mind for future growth:**
- If services become truly independent, consider multi-repo
- Plan for eventual split if team grows to 5+ independent teams
- Document clear module boundaries to avoid tight coupling
- Use workspaces (Nx/Lerna) as an intermediate step
