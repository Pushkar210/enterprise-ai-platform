output "api_endpoint" {
  value = aws_apigatewayv2_api.main.api_endpoint
}

output "health_url" {
  value = "${aws_apigatewayv2_api.main.api_endpoint}/health"
}
