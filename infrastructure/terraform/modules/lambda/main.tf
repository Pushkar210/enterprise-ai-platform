resource "aws_lambda_function" "this" {
  function_name = "${var.project_name}-${var.environment}-${var.lambda_name}"

  filename = "${path.root}/../../${var.source_path}/lambda.zip"

  source_code_hash = filebase64sha256(
    "${path.root}/../../${var.source_path}/lambda.zip"
  )

  role    = var.lambda_role_arn
  handler = "lambda_function.lambda_handler"
  runtime = "python3.13"

  timeout     = 30
  memory_size = 256

  environment {
  variables = {
    DOCUMENTS_TABLE_NAME   = var.table_name
    BUCKET_NAME            = var.bucket_name
    ENVIRONMENT            = var.environment
    LLM_PROVIDER           = "gemini"
    GEMINI_API_KEY_PARAMETER = "/enterprise-ai-platform/gemini-api-key"
  }
}
}