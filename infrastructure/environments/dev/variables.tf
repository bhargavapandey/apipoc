variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "lambda_package_path" {
  description = "Path to Lambda deployment package"
  type        = string
}

variable "layer_arns" {
  description = "ARNs of Lambda layers"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
