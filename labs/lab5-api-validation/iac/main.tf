resource "aws_api_gateway_request_validator" "query_string" {
  name                        = "RequireQueryString"
  rest_api_id                 = var.api_id
  validate_request_parameters = true
}

resource "aws_api_gateway_method" "get_sync" {
  # ... existing props
  request_validator_id = aws_api_gateway_request_validator.query_string.id
  request_parameters = { "method.request.querystring.userID" = true }
}
