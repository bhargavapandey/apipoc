# Branching and Versioning Strategy

## Overview

This document outlines best practices for managing branches, versions, and releases in the halopv-aws-api repository.

## Branching Strategy: Git Flow Model

We follow a modified Git Flow approach optimized for AWS Lambda services:

```
main (production)
 ├── hotfix/
 └── release/v*

staging (pre-production)
 └── develop (integration)
      ├── feature/*
      ├── bugfix/*
      └── experimental/*
```

### Branch Types

#### 1. `main` (Production)

**Purpose**: Production-ready code, deployed to prod environment

**Rules**:
- Protected branch - requires pull request reviews
- Only receives merges from `release/` or `hotfix/` branches
- Every commit is tagged with a version: `v2.1.0`
- Triggers production deployment

**Example PR workflow**:
```bash
# When release is ready
git checkout -b release/v2.1.0 staging
# ... bump versions, update CHANGELOG
git commit -m "Release v2.1.0"
git push origin release/v2.1.0

# After testing, create PR to main
# Once merged:
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0
```

#### 2. `staging` (Pre-production)

**Purpose**: Pre-production validation, staging environment testing

**Rules**:
- Protected branch - requires pull request reviews
- Receives merges from `develop` when ready for staging
- Automatically triggers staging deployment
- Used for UAT (User Acceptance Testing)
- Version tags use pre-release suffix: `v2.1.0-rc.1` (release candidate)

**Typical workflow**:
```bash
git checkout staging
git pull origin staging

# Create release candidate
git checkout -b release/v2.1.0-rc.1 staging
# ... run staging tests
git tag -a v2.1.0-rc.1 -m "Release candidate 1"
```

#### 3. `develop` (Integration)

**Purpose**: Integration branch for feature development

**Rules**:
- Protected branch - requires pull request reviews
- Receives merges from `feature/`, `bugfix/`, and `experimental/` branches
- Automatically triggers dev deployment
- Should always be in a deployable state
- Version tags use development suffix: `v2.1.0-dev.5`

#### 4. Feature Branches (`feature/*`)

**Purpose**: Develop new features or services

**Naming convention**:
```
feature/<domain>-<feature>-<version>
feature/mhra-export-enhancements-v1
feature/icsr-validation-improvements-v2
```

**Lifecycle**:
```bash
# Create from develop
git checkout -b feature/mhra-export-enhancements-v1 develop

# Work on feature
git add .
git commit -m "Add CSV export for MHRA"

# Push and create PR
git push origin feature/mhra-export-enhancements-v1

# After review and CI passes
# Merge to develop via PR
```

#### 5. Bugfix Branches (`bugfix/*`)

**Purpose**: Fix bugs discovered during development

**Naming convention**:
```
bugfix/<issue-id>-<description>
bugfix/ISSUE-123-fix-validation-error
bugfix/ISSUE-456-lambda-timeout-handling
```

**Process**: Same as feature branches, but may be prioritized higher

#### 6. Hotfix Branches (`hotfix/*`)

**Purpose**: Critical fixes for production issues

**Rules**:
- Created from `main` (not develop)
- Can skip staging if critical
- Merged back to both `main` and `staging`/`develop`
- Tagged immediately after merge to main

**Example**:
```bash
# Create from main
git checkout -b hotfix/v2.0.3-lambda-crash main

# Fix issue
git add .
git commit -m "Fix Lambda timeout issue in ICSR handler"

# Create PRs to main and develop
git push origin hotfix/v2.0.3-lambda-crash
```

## Versioning Strategy

### Semantic Versioning

All services follow [Semantic Versioning](https://semver.org/) format: `MAJOR.MINOR.PATCH`

```
v2.1.3
│ │ │
│ │ └─ PATCH: Bug fixes (2.1.2 → 2.1.3)
│ └─── MINOR: New features, backward compatible (2.0 → 2.1)
└───── MAJOR: Breaking changes (1.x → 2.0)
```

### Version Sources

Versioning is maintained in:

#### 1. Service Folder Names

```
src/icsr-submit-e2b-v2/       # Version 2 of ICSR Submit
src/mhra-export-data-v1/      # Version 1 of MHRA Export

infrastructure/services/icsr-submit-api-v2/
infrastructure/services/mhra-export-api-v1/
```

#### 2. Git Tags

**Format**: `v<service>-<version>` or `v<version>` for monorepo releases

```
# Individual service versions
v-icsr-submit-e2b-v2.1.3
v-mhra-export-data-v1.0.5

# Overall release (all services)
v2.1.0    # Released v2.x of all services
```

#### 3. VERSION File (Optional)

```
infrastructure/services/icsr-submit-api-v2/VERSION
2.1.3
```

#### 4. Lambda Environment Variables

```hcl
environment_variables = {
  SERVICE_VERSION = "2.1.3"
  API_VERSION     = "v2"
}
```

### Version Incrementation Rules

| Change | Version | Example | When |
|--------|---------|---------|------|
| Bug fix | PATCH | 2.1.2 → 2.1.3 | Bug fixes only |
| New feature | MINOR | 2.1.0 → 2.2.0 | New endpoints, features |
| Breaking change | MAJOR | 2.0.0 → 3.0.0 | API contract changes, schema changes |
| Pre-release | -rc.N | 2.1.0-rc.1 | Staging, not production ready |
| Development | -dev.N | 2.1.0-dev.5 | Development branch builds |

## Multi-Service Versioning

Since we have multiple services (ICSR, MHRA, etc.), version them independently:

### Per-Service Versioning

```
icsr-submit-e2b:
  - v2.1.3 (current in prod)
  - v2.0.5 (previous in prod)
  
mhra-export-data:
  - v1.2.1 (current in prod)
  - v1.0.0 (previous in prod)
```

### Application-Wide Release

When coordinating multiple service releases, use an application version:

```
halopv-aws-api v2.1.0 release includes:
  - icsr-submit-e2b v2.1.0
  - mhra-export-data v1.1.0
  - requests layer v2.0.0
  - validation layer v2.0.0
```

**Tag structure**:
```bash
# Overall release
git tag -a v2.1.0 -m "HaloPV AWS API v2.1.0
  - ICSR Submit E2B v2.1.0
  - MHRA Export v1.1.0
  - Requests Layer v2.0.0
  - Validation Layer v2.0.0"

# Service-specific
git tag -a icsr-submit-e2b/v2.1.0 -m "ICSR Submit E2B v2.1.0"
git tag -a mhra-export-data/v1.1.0 -m "MHRA Export v1.1.0"
```

## Release Process

### Step 1: Create Release Branch

```bash
# From staging, create release branch
git checkout -b release/v2.1.0 staging

# Bump versions
# - Update VERSION files
# - Update CHANGELOG.md
# - Update service documentation

git add .
git commit -m "Bump version to v2.1.0"
git push origin release/v2.1.0
```

### Step 2: Create Pull Request to Staging

```bash
# PR from release/v2.1.0 → staging
# - Title: "Release: v2.1.0"
# - Description: Changelog summary
# - Triggers staging deployment for final validation
```

### Step 3: Final Testing on Staging

- UAT (User Acceptance Testing)
- Performance testing
- Integration testing
- Security scanning

### Step 4: Merge to Production

```bash
# After staging approval
# PR from release/v2.1.0 → main
# - Requires explicit approval
# - Triggers production deployment
```

### Step 5: Tag and Close Release

```bash
# After merge to main
git checkout main
git pull origin main

# Create version tag
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin v2.1.0

# Merge back to develop
git checkout develop
git pull origin develop
git merge main
git push origin develop

# Delete release branch
git push origin --delete release/v2.1.0
```

## Branch Protection Rules

Configure in GitHub repository settings:

### `main` Branch

- ✅ Require pull request reviews (2 reviewers)
- ✅ Require status checks to pass (CI/CD)
- ✅ Require branches to be up to date before merging
- ✅ Include administrators in restrictions
- ❌ Allow force pushes (never)
- ❌ Allow deletions

### `staging` Branch

- ✅ Require pull request reviews (1 reviewer)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ❌ Allow force pushes

### `develop` Branch

- ✅ Require pull request reviews (1 reviewer)
- ✅ Require status checks to pass
- ❌ Require branches to be up to date (allows fast-forward)
- ❌ Allow force pushes

## Deployment Triggers

### Automatic

| Branch | Environment | Trigger |
|--------|-------------|----------|
| `develop` | dev | Any merge to develop |
| `staging` | staging | Any merge to staging |
| `main` | prod | Any merge to main |

### Manual

```bash
# Deploy specific version to environment
gh workflow run deploy.yml \
  -f environment=prod \
  -f version=v2.1.0
```

## Example Workflow Timeline

```
Week 1: Feature Development
├── Developer: feature/mhra-improvements-v1 → develop
├── CI runs tests, code quality checks
└── Merged after 1 approval

Week 2: Accumulate features
├── Multiple features merged to develop
├── Staging environment gets all changes via auto-deploy
└── Team tests on staging

Week 3: Release Preparation
├── Create release/v2.1.0 from staging
├── Update VERSION, CHANGELOG
├── Merge to staging with all fixes
├── UAT passes on staging
└── Create PR to main

Week 3 (Continued): Production Deployment
├── 2 approvals required
├── Merge to main
├── Auto-deploy to prod
├── Smoke tests pass
├── Tag v2.1.0
└── Merge back to develop

NextWeek: Hotfix (if needed)
├── hotfix/v2.1.1-critical-fix from main
├── Fix and test
├── Merge to main → prod
├── Merge back to develop
└── Close hotfix branch
```

## Tools & Commands

### Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-feature-name
```

### View All Tags

```bash
git tag -l --sort=-version:refname
```

### View Branch History

```bash
git log --graph --oneline --all --decorate
```

### Create Release Notes

```bash
# Show commits between versions
git log v2.0.0..v2.1.0 --oneline
```

## CI/CD Integration

### GitHub Actions Configuration

```yaml
# Deploy on branch merges
on:
  push:
    branches:
      - main      # Production
      - staging   # Staging
      - develop   # Development
```

### Automated Version Bumping (Optional)

Use tools like `semantic-release` or manual `VERSION` files:

```bash
# Automated approach
npm install --save-dev semantic-release

# Manual approach (recommended)
echo "2.1.0" > VERSION
git commit -am "Bump version to 2.1.0"
```

## Best Practices

✅ **Do**
- Use descriptive branch names
- Keep branches short-lived (< 1 week ideally)
- Merge frequently to develop
- Tag releases consistently
- Update CHANGELOG with every release
- Run tests before creating PR
- Use PR descriptions for context

❌ **Don't**
- Commit directly to main/staging/develop
- Create feature branches from main
- Hold onto branches for weeks
- Force push to protected branches
- Mix unrelated changes in one PR
- Skip CI/CD checks
- Deploy without proper versioning

## Troubleshooting

### Accidentally Committed to `develop`

```bash
# Create a new branch from current commit
git branch feature/my-feature

# Reset develop to previous commit
git reset --hard HEAD~1

# Push changes
git push origin feature/my-feature -f
```

### Need to Backport Fix to `main`

```bash
# Create hotfix from main
git checkout -b hotfix/fix-description main

# Cherry-pick commit from develop
git cherry-pick <commit-hash>

# Merge to main and back to develop
```

### Merge Conflicts

```bash
# Pull latest from target branch
git pull origin main

# Resolve conflicts manually
# Mark as resolved
git add <resolved-files>
git commit -m "Resolve merge conflicts"
git push origin feature/my-feature
```

## References

- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
