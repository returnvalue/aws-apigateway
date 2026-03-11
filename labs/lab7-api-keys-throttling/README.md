# Lab 7: Monetization & Security (API Keys & Throttling)

**Goal:** Protect your `prod` stage from DDoS attacks or excessive use by creating a Usage Plan that throttles requests, and generate an API Key that users must pass in their headers to gain access.

```bash
# 1. Create an API Key
KEY_ID=$(awslocal apigateway create-api-key \
  --name "PremiumClientKey" \
  --enabled \
  --query 'id' --output text)

# 2. Create a Usage Plan with strict Rate Limiting (5 requests/sec, burst to 10)
PLAN_ID=$(awslocal apigateway create-usage-plan \
  --name "PremiumTierPlan" \
  --api-stages apiId=$API_ID,stage=prod \
  --throttle burstLimit=10,rateLimit=5 \
  --quota limit=1000,offset=0,period=MONTH \
  --query 'id' --output text)

# 3. Associate the API Key with the Usage Plan
awslocal apigateway create-usage-plan-key \
  --usage-plan-id $PLAN_ID \
  --key-id $KEY_ID \
  --key-type "API_KEY"

# 4. Enforce the API Key requirement on the /sync endpoint
awslocal apigateway update-method \
  --rest-api-id $API_ID \
  --resource-id $SYNC_ID \
  --http-method GET \
  --patch-operations "op=replace,path=/apiKeyRequired,value=true"

# 5. Redeploy the API to 'prod' to apply the API Key enforcement
awslocal apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod
```

## 🧠 Key Concepts & Importance

- **API Keys:** Alphanumeric strings that you distribute to application developer customers to grant access to your API.
- **Usage Plans:** Define who can access one or more deployed API stages and methods—and also how much and how fast they can access them.
- **Throttling (Token Bucket Algorithm):**
    - **Rate Limit:** The steady-state request rate (average requests per second).
    - **Burst Limit:** The maximum number of concurrent requests API Gateway can handle at a single moment.
- **Quotas:** The maximum number of requests that can be made in a given time period (day, week, or month).
- **Security & Monetization:** Usage plans allow you to protect your backend from being overwhelmed and provide a mechanism to offer different tiers of service (e.g., Free vs. Premium) to your customers.

## 🛠️ Command Reference

- `apigateway create-api-key`: Creates a unique key for client identification.
- `apigateway create-usage-plan`: Creates a plan that enforces throttling and quotas.
    - `--api-stages`: Associates the plan with a specific API and Stage.
    - `--throttle`: Sets the rate and burst limits.
    - `--quota`: Sets the maximum number of requests for a time period.
- `apigateway create-usage-plan-key`: Links a specific API Key to a Usage Plan.
- `apigateway update-method`: Used here to set `apiKeyRequired=true`.
- `apigateway create-deployment`: Necessary to push the `apiKeyRequired` configuration change to the live stage.
