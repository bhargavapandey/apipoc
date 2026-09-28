variable "api_name" {
  description = "Name of the API Gateway"
  type        = string
}

variable "stage_name" {
  description = "Stage name (e.g., dev, staging, prod)"
  type        = string
}

variable "lambda_arn" {
  description = "ARN of the Lambda function to integrate"
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "route_key" {
  description = "Route key (e.g., 'POST /submit')"
  type        = string
}

variable "description" {
  description = "Description of the API"
  type        = string
  default     = ""
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 7
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
