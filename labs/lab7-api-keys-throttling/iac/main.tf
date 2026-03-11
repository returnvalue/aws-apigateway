resource "aws_api_gateway_api_key" "premium" {
  name    = "PremiumClientKey"
  enabled = true
}

resource "aws_api_gateway_usage_plan" "premium" {
  name = "PremiumTierPlan"
  api_stages {
    api_id = var.api_id
    stage  = "prod"
  }
  throttle_settings {
    burst_limit = 10
    rate_limit  = 5
  }
  quota_settings {
    limit  = 1000
    period = "MONTH"
  }
}

resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.premium.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.premium.id
}
