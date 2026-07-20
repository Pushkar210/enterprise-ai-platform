data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.root}/../../${var.source_path}"
  output_path = "${path.root}/../../${var.source_path}/lambda.zip"
}

resource "aws_lambda_function" "this" {
  function_name = "${var.project_name}-${var.environment}-${var.lambda_name}"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

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
    data.archive_file.lambda_zip
  ]
}