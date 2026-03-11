resource "aws_sqs_queue" "ingestion" {
  name = "IngestionQueue"
}

resource "aws_iam_role" "apigw_sqs" {
  name = "ApiGatewayDirectRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole", Effect = "Allow", Principal = { Service = "apigateway.amazonaws.com" } }]
  })
}

resource "aws_iam_role_policy" "sqs_send" {
  name = "SQSAccess"
  role = aws_iam_role.apigw_sqs.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Action = "sqs:SendMessage", Effect = "Allow", Resource = aws_sqs_queue.ingestion.arn }]
  })
}

resource "aws_api_gateway_integration" "sqs" {
  rest_api_id = var.api_id
  resource_id = var.resource_id
  http_method = "POST"
  type        = "AWS"
  integration_http_method = "POST"
  uri         = "arn:aws:apigateway:${var.region}:sqs:path/${var.account_id}/${aws_sqs_queue.ingestion.name}"
  credentials = aws_iam_role.apigw_sqs.arn
  request_parameters = { "integration.request.header.Content-Type" = "'application/x-www-form-urlencoded'" }
  request_templates = { "application/json" = "Action=SendMessage&MessageBody=$util.urlEncode($input.body)" }
}
