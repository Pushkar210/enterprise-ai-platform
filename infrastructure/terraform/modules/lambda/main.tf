data "archive_file" "upload_lambda" {
  type        = "zip"
  source_dir  = "${path.root}/../../backend/lambda/upload"
  output_path = "${path.root}/../../backend/lambda/upload/lambda.zip"
}

resource "aws_lambda_function" "upload" {
  function_name = "${var.project_name}-${var.environment}-upload"

  filename         = data.archive_file.upload_lambda.output_path
  source_code_hash = data.archive_file.upload_lambda.output_base64sha256

  role    = var.lambda_role_arn
  handler = "lambda_function.lambda_handler"
  runtime = "python3.13"

  timeout     = 30
  memory_size = 256

  environment {
  variables = {
    DOCUMENTS_TABLE_NAME = var.table_name
    BUCKET_NAME          = var.bucket_name
    ENVIRONMENT          = var.environment
  }
}

  depends_on = [
    data.archive_file.upload_lambda
  ]
}