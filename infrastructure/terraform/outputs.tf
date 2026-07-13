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