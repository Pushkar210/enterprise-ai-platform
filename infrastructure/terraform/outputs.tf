output "bucket_name" {
  value = module.s3.bucket_name
}

output "bucket_arn" {
  value = module.s3.bucket_arn
}

output "table_name" {
  value = module.dynamodb.table_name
}

output "table_arn" {
  value = module.dynamodb.table_arn
}

output "lambda_role_arn" {
  value = module.iam.lambda_role_arn
}

output "lambda_role_name" {
  value = module.iam.lambda_role_name
} 

output "api_lambda_function_name" {
  value = module.api_lambda.lambda_function_name
}

output "api_lambda_function_arn" {
  value = module.api_lambda.lambda_function_arn
}

output "api_lambda_invoke_arn" {
  value = module.api_lambda.lambda_invoke_arn
}

output "processor_lambda_function_name" {
  value = module.processor_lambda.lambda_function_name
}

output "processor_lambda_function_arn" {
  value = module.processor_lambda.lambda_function_arn
}

output "processor_lambda_invoke_arn" {
  value = module.processor_lambda.lambda_invoke_arn
}

output "api_endpoint" {
  value = module.apigateway.api_endpoint
}

output "health_url" {
  value = module.apigateway.health_url
}
