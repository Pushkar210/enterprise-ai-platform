module "s3" {
  source = "./modules/s3"

  bucket_name  = "${var.project_name}-${var.environment}-documents"
  project_name = var.project_name
  environment  = var.environment
}