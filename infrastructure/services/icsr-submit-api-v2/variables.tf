variable "environment" {
  description = "Deployment environment"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "lambda_package_path" {
  description = "Path to Lambda deployment package"
  type        = string
}

variable "api_endpoint" {
  description = "API endpoint URL"
  type        = string
}

variable "log_level" {
  description = "Log level for Lambda function"
  type        = string
  default     = "INFO"
}

variable "layer_arns" {
  description = "ARNs of Lambda layers to attach"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
