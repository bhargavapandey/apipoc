aws_region          = "us-east-1"
lambda_package_path = "../../build/icsr-submit-e2b-v2.zip"
layer_arns          = [
  # Add layer ARNs when available
  # "arn:aws:lambda:us-east-1:123456789012:layer:halopv-requests-v2-layer:1"
]

tags = {
  Application = "ICSR Submit API"
  Version     = "v2"
  Owner       = "Development Team"
  CostCenter  = "Engineering"
}
