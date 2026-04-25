# Lab 3: Fan-Out Webhooks (Direct SNS Integration)

**Goal:** Expose an endpoint that receives a payload and publishes it directly to an SNS Topic, which can then fan out to SMS, Email, or SQS subscribers.

```bash
# 1. Create the target SNS Topic
TOPIC_ARN=$(awslocal sns create-topic --name BroadcastTopic --query 'TopicArn' --output text)
TOPIC_ARN=$(aws sns create-topic --name BroadcastTopic --query 'TopicArn' --output text)

# 2. Add SNS permissions to our existing API Gateway Role
awslocal iam put-role-policy --role-name ApiGatewayDirectRole --policy-name SNSAccess --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"sns:Publish","Resource":"*"}]}'
aws iam put-role-policy --role-name ApiGatewayDirectRole --policy-name SNSAccess --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"sns:Publish","Resource":"*"}]}'

# 3. Create the /broadcast resource and POST method
BROADCAST_ID=$(awslocal apigateway create-resource --rest-api-id $API_ID --parent-id $PARENT_ID --path-part "broadcast" --query 'id' --output text)
BROADCAST_ID=$(aws apigateway create-resource --rest-api-id $API_ID --parent-id $PARENT_ID --path-part "broadcast" --query 'id' --output text)
awslocal apigateway put-method --rest-api-id $API_ID --resource-id $BROADCAST_ID --http-method POST --authorization-type NONE
aws apigateway put-method --rest-api-id $API_ID --resource-id $BROADCAST_ID --http-method POST --authorization-type NONE

# 4. Integrate directly with SNS using VTL mapping
awslocal apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $BROADCAST_ID \
  --http-method POST \
  --type AWS \
  --integration-http-method POST \
  --uri "arn:aws:apigateway:us-east-1:sns:action/Publish" \
  --credentials $APIGW_ROLE \
  --request-parameters '{"integration.request.header.Content-Type": "'\''application/x-www-form-urlencoded'\''"}' \
  --request-templates '{"application/json": "Action=Publish&TopicArn=$util.urlEncode('\'$TOPIC_ARN\'')&Message=$util.urlEncode($input.body)"}'
aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $BROADCAST_ID \
  --http-method POST \
  --type AWS \
  --integration-http-method POST \
  --uri "arn:aws:apigateway:us-east-1:sns:action/Publish" \
  --credentials $APIGW_ROLE \
  --request-parameters '{"integration.request.header.Content-Type": "'\''application/x-www-form-urlencoded'\''"}' \
  --request-templates '{"application/json": "Action=Publish&TopicArn=$util.urlEncode('\'$TOPIC_ARN\'')&Message=$util.urlEncode($input.body)"}'

awslocal apigateway put-method-response --rest-api-id $API_ID --resource-id $BROADCAST_ID --http-method POST --status-code 200
aws apigateway put-method-response --rest-api-id $API_ID --resource-id $BROADCAST_ID --http-method POST --status-code 200
awslocal apigateway put-integration-response --rest-api-id $API_ID --resource-id $BROADCAST_ID --http-method POST --status-code 200 --selection-pattern ""
aws apigateway put-integration-response --rest-api-id $API_ID --resource-id $BROADCAST_ID --http-method POST --status-code 200 --selection-pattern ""
```

## 🧠 Key Concepts & Importance

- **Fan-Out Pattern:** A messaging pattern where a single message is sent to an SNS topic and then distributed (fanned out) to multiple subscribers or endpoints.
- **Webhook Ingestion:** Using API Gateway as a public-facing entry point for webhooks, allowing third-party services to trigger internal AWS workflows.
- **Decoupled Broadcasting:** The sender only needs to know about the API endpoint. The logic for who receives the message (email, Lambda, SQS) is managed by SNS subscriptions.
- **Scalability:** SNS can handle massive numbers of messages and subscribers, making it ideal for notification systems or event-driven architectures.

## 🛠️ Command Reference

- `sns create-topic`: Creates a logical access point and communication channel.
- `iam put-role-policy`: Adds or updates an inline policy for a specific IAM role.
- `apigateway create-resource`: Adds a new path segment to the API.
- `apigateway put-method`: Configures an HTTP method for an API resource.
- `apigateway put-integration`: Sets up the backend integration (direct SNS `Publish` action).
    - `--uri`: For SNS, uses the `sns:action/Publish` syntax.
    - `--request-templates`: Uses VTL to map the incoming body to the `Message` parameter and includes the `TopicArn`.
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
