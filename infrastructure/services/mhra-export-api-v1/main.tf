# MHRA Export API v1 Service Definition

locals {
  app_name           = "halopv"
  domain             = "mhra"
  function           = "export-data"
  version            = "v1"
  function_name      = "${local.app_name}-${local.domain}-${local.function}-${local.version}-lambda"
  api_name           = "${local.app_name}-${local.domain}-api-${local.version}"
  export_bucket      = "${local.app_name}-exports-${var.environment}"
}

module "lambda" {
  source = "../modules/lambda"

  function_name = local.function_name
  description   = "MHRA data export for submissions (v1)"
  
  lambda_package_path = var.lambda_package_path
  handler             = "lambda_function.lambda_handler"
  runtime             = "python3.11"
  timeout             = 300  # 5 minutes for export processing
  memory_size         = 1024 # Higher memory for data processing

  environment_variables = {
    EXPORT_BUCKET   = aws_s3_bucket.exports.id
    EXPORT_FORMAT   = "csv"
    LOG_LEVEL       = var.log_level
  }

  layer_arns = var.layer_arns
  policy_document = data.aws_iam_policy_document.lambda_policy.json
  
  tags = merge(
    var.tags,
    {
      Environment = var.environment
      Service     = "mhra-export"
      Version     = local.version
    }
  )
}

resource "aws_s3_bucket" "exports" {
  bucket = local.export_bucket

  tags = merge(
    var.tags,
    {
      Name = local.export_bucket
    }
  )
}

resource "aws_s3_bucket_versioning" "exports" {
  bucket = aws_s3_bucket.exports.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "exports" {
  bucket = aws_s3_bucket.exports.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

module "api_gateway" {
  source = "../modules/api_gateway"

  api_name            = local.api_name
  stage_name          = var.environment
  lambda_arn          = module.lambda.function_arn
  lambda_function_name = module.lambda.function_name
  route_key           = "POST /mhra/export"
  description         = "MHRA data export API (v1)"

  tags = merge(
    var.tags,
    {
      Environment = var.environment
      Service     = "mhra-export"
      Version     = local.version
    }
  )
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    sid = "CloudWatchLogs"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }

  statement {
    sid = "S3Export"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.exports.arn,
      "${aws_s3_bucket.exports.arn}/*"
    ]
  }

  statement {
    sid = "CloudWatchMetrics"
    actions = [
      "cloudwatch:PutMetricData"
    ]
    resources = ["*"]
  }
}
