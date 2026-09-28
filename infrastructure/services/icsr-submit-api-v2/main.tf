# ICSR Submit API v2 Service Definition

locals {
  app_name           = "halopv"
  domain             = "icsr"
  function           = "submit-e2b"
  version            = "v2"
  function_name      = "${local.app_name}-${local.domain}-${local.function}-${local.version}-lambda"
  api_name           = "${local.app_name}-${local.domain}-api-${local.version}"
}

module "lambda" {
  source = "../modules/lambda"

  function_name = local.function_name
  description   = "ICSR submission with E2B format validation (v2)"
  
  lambda_package_path = var.lambda_package_path
  handler             = "lambda_function.lambda_handler"
  runtime             = "python3.11"
  timeout             = 60
  memory_size         = 512

  environment_variables = {
    API_ENDPOINT               = var.api_endpoint
    VALIDATION_SCHEMA_VERSION  = "2.0"
    LOG_LEVEL                  = var.log_level
  }

  layer_arns = var.layer_arns

  policy_document = data.aws_iam_policy_document.lambda_policy.json
  
  tags = merge(
    var.tags,
    {
      Environment = var.environment
      Service     = "icsr-submit"
      Version     = local.version
    }
  )
}

module "api_gateway" {
  source = "../modules/api_gateway"

  api_name            = local.api_name
  stage_name          = var.environment
  lambda_arn          = module.lambda.function_arn
  lambda_function_name = module.lambda.function_name
  route_key           = "POST /icsr/submit"
  description         = "ICSR submission API (v2)"

  tags = merge(
    var.tags,
    {
      Environment = var.environment
      Service     = "icsr-submit"
      Version     = local.version
    }
  )
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }

  statement {
    actions = [
      "cloudwatch:PutMetricData"
    ]
    resources = ["*"]
  }
}
