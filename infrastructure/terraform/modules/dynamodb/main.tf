resource "aws_dynamodb_table" "documents" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "document_id"

  attribute {
    name = "document_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Name        = "Document Metadata"
    Project     = var.project_name
    Environment = var.environment
  }
}