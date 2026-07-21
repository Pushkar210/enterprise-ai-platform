module "s3" {
  source = "./modules/s3"

  bucket_name  = "${var.project_name}-${var.environment}-documents"
  project_name = var.project_name
  environment  = var.environment
}

module "dynamodb" {
  source = "./modules/dynamodb"

  table_name   = "${var.project_name}-${var.environment}-documents"
  project_name = var.project_name
  environment  = var.environment
}

module "iam" {
  source = "./modules/iam"

  project_name = var.project_name
  environment  = var.environment

  bucket_arn = module.s3.bucket_arn
  table_arn  = module.dynamodb.table_arn
}

module "api_lambda" {
  source = "./modules/lambda"

  project_name    = var.project_name
  environment     = var.environment
  lambda_role_arn = module.iam.lambda_role_arn
  table_name      = module.dynamodb.table_name
  bucket_name     = module.s3.bucket_name

  lambda_name = "api"
  source_path = "backend/lambda/api" 
}

module "processor_lambda" {
  source = "./modules/lambda"

  project_name    = var.project_name
  environment     = var.environment
  lambda_role_arn = module.iam.lambda_role_arn
  table_name      = module.dynamodb.table_name
  bucket_name     = module.s3.bucket_name

  lambda_name = "processor"
  source_path = "backend/lambda/processor"
}

resource "aws_lambda_permission" "allow_s3_processor" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = module.processor_lambda.lambda_function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.s3.bucket_arn
}

resource "aws_s3_bucket_notification" "processor_trigger" {
  bucket = module.s3.bucket_name

  lambda_function {
    lambda_function_arn = module.processor_lambda.lambda_function_arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_lambda_permission.allow_s3_processor
  ]
}

module "apigateway" {
  source = "./modules/apigateway"

  project_name         = var.project_name
  environment          = var.environment
  lambda_function_name = module.api_lambda.lambda_function_name
  lambda_invoke_arn    = module.api_lambda.lambda_invoke_arn
}