resource "aws_cloudwatch_event_bus" "webhook" {
  name = "WebhookBus"
}

resource "aws_api_gateway_integration" "eventbridge" {
  rest_api_id = var.api_id
  resource_id = var.resource_id
  http_method = "POST"
  type        = "AWS"
  integration_http_method = "POST"
  uri         = "arn:aws:apigateway:${var.region}:events:action/PutEvents"
  credentials = var.role_arn
  request_parameters = { "integration.request.header.Content-Type" = "'application/x-www-form-urlencoded'" }
  request_templates = { "application/json" = "Action=PutEvents&Version=2015-10-07&Event.1.Source=api.gateway&Event.1.EventBusName=${aws_cloudwatch_event_bus.webhook.name}&Event.1.DetailType=WebhookReceived&Event.1.Detail=$util.urlEncode($input.body)" }
}
