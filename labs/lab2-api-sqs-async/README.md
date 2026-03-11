# Lab 2: Storage-First Pattern (Direct SQS Integration)

**Goal:** Bypass Lambda entirely for high-volume ingestion. Configure API Gateway to transform an incoming HTTP POST request into an `Action=SendMessage` payload and drop it directly into an SQS Queue to absorb massive traffic spikes.

```bash
# 1. Create the target SQS Queue
ACCOUNT_ID=$(awslocal sts get-caller-identity --query 'Account' --output text)
awslocal sqs create-queue --queue-name IngestionQueue

# 2. Create an IAM Role allowing API Gateway to write to SQS
APIGW_ROLE=$(awslocal iam create-role --role-name ApiGatewayDirectRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"apigateway.amazonaws.com"},"Action":"sts:AssumeRole"}]}' --query 'Role.Arn' --output text)
awslocal iam put-role-policy --role-name ApiGatewayDirectRole --policy-name SQSAccess --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"sqs:SendMessage","Resource":"*"}]}'

# 3. Create the /async resource and POST method
ASYNC_ID=$(awslocal apigateway create-resource --rest-api-id $API_ID --parent-id $PARENT_ID --path-part "async" --query 'id' --output text)
awslocal apigateway put-method --rest-api-id $API_ID --resource-id $ASYNC_ID --http-method POST --authorization-type NONE

# 4. Create the Direct AWS Integration with Velocity Template Language (VTL) mapping
awslocal apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $ASYNC_ID \
  --http-method POST \
  --type AWS \
  --integration-http-method POST \
  --uri "arn:aws:apigateway:us-east-1:sqs:path/${ACCOUNT_ID}/IngestionQueue" \
  --credentials $APIGW_ROLE \
  --request-parameters '{"integration.request.header.Content-Type": "'\''application/x-www-form-urlencoded'\''"}' \
  --request-templates '{"application/json": "Action=SendMessage&MessageBody=$util.urlEncode($input.body)"}'

# 5. Set the Method Response to 200 OK
awslocal apigateway put-method-response --rest-api-id $API_ID --resource-id $ASYNC_ID --http-method POST --status-code 200
awslocal apigateway put-integration-response --rest-api-id $API_ID --resource-id $ASYNC_ID --http-method POST --status-code 200 --selection-pattern ""
```

## 🧠 Key Concepts & Importance

- **Storage-First Pattern:** A design pattern where incoming requests are immediately stored in a durable queue or database before processing. This ensures that the system can handle bursts of traffic without overwhelming backend compute resources.
- **Direct AWS Integration:** API Gateway can communicate directly with other AWS services (like SQS, Kinesis, or DynamoDB) without requiring a Lambda function. This reduces latency, cost, and code maintenance.
- **VTL (Velocity Template Language):** A templating engine used by API Gateway to transform request and response payloads. In this lab, we use VTL to convert a JSON body into the URL-encoded format required by the SQS Query API.
- **Mapping Templates:** Allow you to redefine the structure of the data as it passes through API Gateway.
- **Credential Passthrough:** API Gateway uses an IAM role to authorize the action against the downstream AWS service.

## 🛠️ Command Reference

- `sqs create-queue`: Provisions a new message queue.
- `iam put-role-policy`: Attaches an inline permissions policy to a role.
- `apigateway put-integration`: Configures the backend connection.
    - `--type AWS`: Indicates a direct integration with an AWS service.
    - `--credentials`: The IAM role ARN API Gateway assumes to perform the action.
    - `--request-templates`: The VTL mapping used to transform the payload.
- `apigateway put-method-response`: Defines the HTTP response configuration for the method.
- `apigateway put-integration-response`: Maps the backend response to the method response.
