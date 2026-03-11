resource "aws_api_gateway_deployment" "dev" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  description = "Initial Development Deployment"
  lifecycle { create_before_destroy = true }
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.dev.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = "dev"
}
