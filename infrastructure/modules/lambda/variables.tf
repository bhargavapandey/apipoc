variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "lambda_package_path" {
  description = "Path to the Lambda deployment package"
  type        = string
}

variable "handler" {
  description = "Lambda handler"
  type        = string
  default     = "lambda_function.lambda_handler"
}

variable "runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.11"
}

variable "timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 60
}

variable "memory_size" {
  description = "Lambda memory in MB"
  type        = number
  default     = 256
}

variable "description" {
  description = "Description of the Lambda function"
  type        = string
  default     = ""
}

variable "environment_variables" {
  description = "Environment variables for Lambda"
  type        = map(string)
  default     = {}
}

variable "layer_arns" {
  description = "ARNs of Lambda layers to attach"
  type        = list(string)
  default     = []
}

variable "policy_document" {
  description = "IAM policy document for Lambda execution role"
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
