# Lambda function module

resource "aws_lambda_function" "this" {
  filename         = var.lambda_package_path
  function_name    = var.function_name
  role             = aws_iam_role.lambda_role.arn
  handler          = var.handler
  source_code_hash = filebase64sha256(var.lambda_package_path)
  timeout          = var.timeout
  memory_size      = var.memory_size
  runtime          = var.runtime
  description      = var.description

  environment {
    variables = var.environment_variables
  }

  layers = var.layer_arns

  tags = merge(
    var.tags,
    {
      Name = var.function_name
    }
  )
}

resource "aws_iam_role" "lambda_role" {
  name = "${var.function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Attach additional policies if provided
resource "aws_iam_role_policy" "custom" {
  count  = var.policy_document != null ? 1 : 0
  name   = "${var.function_name}-policy"
  role   = aws_iam_role.lambda_role.id
  policy = var.policy_document
}
