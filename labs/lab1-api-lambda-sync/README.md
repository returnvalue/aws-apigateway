# Lab 1: Foundational API & Synchronous Lambda

**Goal:** Create the root REST API, deploy a simple Python Lambda function, and connect them using a Proxy Integration.

```bash
# 1. Create a basic Lambda function
cat <<EOF > api_handler.py
import json
def lambda_handler(event, context):
    return {"statusCode": 200, "body": json.dumps({"message": "Synchronous response from Lambda!"})}
EOF
zip function.zip api_handler.py

# 2. Create the IAM Execution Role and Lambda Function
ROLE_ARN=$(awslocal iam create-role --role-name APILambdaRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' --query 'Role.Arn' --output text)
LAMBDA_ARN=$(awslocal lambda create-function --function-name ApiCompute --runtime python3.9 --role $ROLE_ARN --handler api_handler.lambda_handler --zip-file fileb://function.zip --query 'FunctionArn' --output text)

# 3. Create the REST API and capture the Root Resource ID
API_ID=$(awslocal apigateway create-rest-api --name "EnterpriseAPI" --query 'id' --output text)
PARENT_ID=$(awslocal apigateway get-resources --rest-api-id $API_ID --query 'items[0].id' --output text)

# 4. Create a /sync resource and GET method
SYNC_ID=$(awslocal apigateway create-resource --rest-api-id $API_ID --parent-id $PARENT_ID --path-part "sync" --query 'id' --output text)
awslocal apigateway put-method --rest-api-id $API_ID --resource-id $SYNC_ID --http-method GET --authorization-type NONE

# 5. Connect the GET method to the Lambda function
awslocal apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $SYNC_ID \
  --http-method GET \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations
```

## 🧠 Key Concepts & Importance

- **REST API:** A collection of HTTP resources and methods that are integrated with backend HTTP endpoints, Lambda functions, or other AWS services.
- **Lambda Proxy Integration:** The simplest way to integrate API Gateway with Lambda. API Gateway passes the entire incoming request to the Lambda function as-is, and the Lambda function must return a response in a specific format.
- **Resources & Methods:** Resources represent paths (e.g., `/sync`), and methods represent HTTP verbs (e.g., `GET`, `POST`).
- **Integrations:** Define how API Gateway communicates with the backend. For Lambda, the integration-http-method is always `POST`.

## 🛠️ Command Reference

- `iam create-role`: Creates an IAM execution role for the Lambda function.
- `lambda create-function`: Provisions the serverless compute resource.
- `apigateway create-rest-api`: Initializes a new REST API container.
    - `--name`: The display name of the API.
- `apigateway get-resources`: Retrieves the resources of an API (used here to find the root `/`).
- `apigateway create-resource`: Creates a new path segment.
    - `--path-part`: The URL slug (e.g., `sync`).
- `apigateway put-method`: Defines an HTTP method for a resource.
    - `--http-method`: The verb (e.g., `GET`).
    - `--authorization-type`: Security setting (e.g., `NONE`).
- `apigateway put-integration`: Maps the API method to the backend.
    - `--type`: Integration type (e.g., `AWS_PROXY`).
    - `--uri`: The ARN of the backend service to trigger.
