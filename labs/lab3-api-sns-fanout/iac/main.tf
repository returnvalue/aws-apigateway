resource "aws_sns_topic" "broadcast" {
  name = "BroadcastTopic"
}

resource "aws_api_gateway_integration" "sns" {
  rest_api_id = var.api_id
  resource_id = var.resource_id
  http_method = "POST"
  type        = "AWS"
  integration_http_method = "POST"
  uri         = "arn:aws:apigateway:${var.region}:sns:action/Publish"
  credentials = var.role_arn
  request_parameters = { "integration.request.header.Content-Type" = "'application/x-www-form-urlencoded'" }
  request_templates = { "application/json" = "Action=Publish&TopicArn=$util.urlEncode('${aws_sns_topic.broadcast.arn}')&Message=$util.urlEncode($input.body)" }
}
