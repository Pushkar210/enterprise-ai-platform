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

module "lambda" {
  source = "./modules/lambda"

  project_name    = var.project_name
  environment     = var.environment
  lambda_role_arn = module.iam.lambda_role_arn
}

module "apigateway" {
  source = "./modules/apigateway"

  project_name         = var.project_name
  environment          = var.environment
  lambda_function_name = module.lambda.lambda_function_name
  lambda_invoke_arn    = module.lambda.lambda_invoke_arn
}