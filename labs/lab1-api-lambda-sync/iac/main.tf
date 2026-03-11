resource "aws_api_gateway_rest_api" "main" {
  name = "EnterpriseAPI"
}

resource "aws_api_gateway_resource" "sync" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "sync"
}

resource "aws_api_gateway_method" "get_sync" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.sync.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = aws_api_gateway_resource.sync.id
  http_method             = aws_api_gateway_method.get_sync.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_function_invoke_arn
}
