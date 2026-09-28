output "api_id" {
  description = "API Gateway ID"
  value       = aws_apigatewayv2_api.this.id
}

output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_stage.this.invoke_url
}

output "stage_name" {
  description = "Stage name"
  value       = aws_apigatewayv2_stage.this.name
}
