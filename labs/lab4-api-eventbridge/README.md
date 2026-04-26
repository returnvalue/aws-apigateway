# Lab 4: Event Routing (Direct EventBridge Integration)

**Goal:** Expose an endpoint designed to ingest third-party webhooks (like Stripe or GitHub) directly onto an EventBridge Custom Bus, enabling event-driven routing across your organization.
```bash
# 1. Create a Custom EventBus
awslocal events create-event-bus --name WebhookBus
aws events create-event-bus --name WebhookBus

# 2. Add EventBridge permissions to our existing API Gateway Role
awslocal iam put-role-policy --role-name ApiGatewayDirectRole --policy-name EventBridgeAccess --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"events:PutEvents","Resource":"*"}]}'
aws iam put-role-policy --role-name ApiGatewayDirectRole --policy-name EventBridgeAccess --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"events:PutEvents","Resource":"*"}]}'

# 3. Create the /events resource and POST method
EVENT_ID=$(awslocal apigateway create-resource --rest-api-id $API_ID --parent-id $PARENT_ID --path-part "events" --query 'id' --output text)
EVENT_ID=$(aws apigateway create-resource --rest-api-id $API_ID --parent-id $PARENT_ID --path-part "events" --query 'id' --output text)
awslocal apigateway put-method --rest-api-id $API_ID --resource-id $EVENT_ID --http-method POST --authorization-type NONE
aws apigateway put-method --rest-api-id $API_ID --resource-id $EVENT_ID --http-method POST --authorization-type NONE

# 4. Integrate with EventBridge PutEvents
awslocal apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $EVENT_ID \
  --http-method POST \
  --type AWS \
  --integration-http-method POST \
  --uri "arn:aws:apigateway:us-east-1:events:action/PutEvents" \
  --credentials $APIGW_ROLE \
  --request-parameters '{"integration.request.header.Content-Type": "'\''application/x-www-form-urlencoded'\''"}' \
  --request-templates '{"application/json": "Action=PutEvents&Version=2015-10-07&Event.1.Source=api.gateway&Event.1.EventBusName=WebhookBus&Event.1.DetailType=WebhookReceived&Event.1.Detail=$util.urlEncode($input.body)"}'
aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $EVENT_ID \
  --http-method POST \
  --type AWS \
  --integration-http-method POST \
  --uri "arn:aws:apigateway:us-east-1:events:action/PutEvents" \
  --credentials $APIGW_ROLE \
  --request-parameters '{"integration.request.header.Content-Type": "'\''application/x-www-form-urlencoded'\''"}' \
  --request-templates '{"application/json": "Action=PutEvents&Version=2015-10-07&Event.1.Source=api.gateway&Event.1.EventBusName=WebhookBus&Event.1.DetailType=WebhookReceived&Event.1.Detail=$util.urlEncode($input.body)"}'

awslocal apigateway put-method-response --rest-api-id $API_ID --resource-id $EVENT_ID --http-method POST --status-code 200
aws apigateway put-method-response --rest-api-id $API_ID --resource-id $EVENT_ID --http-method POST --status-code 200
awslocal apigateway put-integration-response --rest-api-id $API_ID --resource-id $EVENT_ID --http-method POST --status-code 200 --selection-pattern ""
aws apigateway put-integration-response --rest-api-id $API_ID --resource-id $EVENT_ID --http-method POST --status-code 200 --selection-pattern ""
```

## 🧠 Key Concepts & Importance

- **Amazon EventBridge:** A serverless event bus that makes it easy to connect applications together using data from your own applications, integrated SaaS applications, and AWS services.
- **Custom Event Bus:** A specialized event bus you create to receive events from your own applications or webhooks.
- **Event-Driven Architecture:** Direct integration with EventBridge allows you to react to incoming data by defining rules that route events to targets like Lambda, SQS, or Step Functions.
- **Scalable Ingestion:** Similar to SQS, direct EventBridge integration allows for high-throughput ingestion without the cold-start overhead or concurrency limits of Lambda.
- **VTL Payload Construction:** The `PutEvents` action requires a specific array structure (`Event.1.Source`, `Event.1.Detail`, etc.). VTL is used to map the flat HTTP body into this structured format.

## 🛠️ Command Reference

- `events create-event-bus`: Creates a new custom event bus.
- `iam put-role-policy`: Updates the API Gateway role to include `events:PutEvents` permissions.
- `apigateway put-integration`: Configures the backend integration (direct EventBridge `PutEvents` action).
    - `--uri`: For EventBridge, uses the `events:action/PutEvents` syntax.
    - `--request-templates`: Maps the request to the required EventBridge wire format.
- `apigateway put-method-response`: Configures the method response.
- `apigateway put-integration-response`: Configures the integration response.

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
