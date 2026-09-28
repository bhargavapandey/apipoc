# Staging Environment Configuration

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "halopv-terraform-state-staging"
    key            = "icsr-submit-api-v2/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "HaloPV"
      Environment = "staging"
      ManagedBy   = "Terraform"
    }
  }
}

module "icsr_submit_api" {
  source = "../../services/icsr-submit-api-v2"

  environment           = "staging"
  lambda_package_path   = var.lambda_package_path
  api_endpoint          = "https://staging-api.halopv.example.com"
  log_level             = "INFO"
  layer_arns            = var.layer_arns

  tags = var.tags
}
