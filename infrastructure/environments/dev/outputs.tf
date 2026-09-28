output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = module.icsr_submit_api.lambda_function_arn
}

output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = module.icsr_submit_api.api_endpoint
}
