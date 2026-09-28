output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = module.lambda.function_arn
}

output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = module.api_gateway.api_endpoint
}

output "export_bucket_name" {
  description = "S3 bucket for exports"
  value       = aws_s3_bucket.exports.id
}
