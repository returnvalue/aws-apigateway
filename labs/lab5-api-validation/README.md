# Lab 5: Payload Edge Validation

**Goal:** Reduce compute costs and protect backend resources by rejecting malformed requests at the API Gateway level. We will enforce that the `/sync` endpoint must contain a specific query string parameter.

```bash
# 1. Create a Request Validator for Query Strings
VALIDATOR_ID=$(awslocal apigateway create-request-validator \
  --rest-api-id $API_ID \
  --name "RequireQueryString" \
  --validate-request-parameters \
  --query 'id' --output text)
VALIDATOR_ID=$(aws apigateway create-request-validator \
  --rest-api-id $API_ID \
  --name "RequireQueryString" \
  --validate-request-parameters \
  --query 'id' --output text)

# 2. Update the /sync GET method to require a parameter named 'userID'
awslocal apigateway update-method \
  --rest-api-id $API_ID \
  --resource-id $SYNC_ID \
  --http-method GET \
  --patch-operations "op=add,path=/requestParameters/method.request.querystring.userID,value=true" \
                     "op=replace,path=/requestValidatorId,value=$VALIDATOR_ID"
aws apigateway update-method \
  --rest-api-id $API_ID \
  --resource-id $SYNC_ID \
  --http-method GET \
  --patch-operations "op=add,path=/requestParameters/method.request.querystring.userID,value=true" \
                     "op=replace,path=/requestValidatorId,value=$VALIDATOR_ID"

# (Now, any request to /sync without ?userID=123 will receive a 
# 400 Bad Request directly from API Gateway!)
```

## 🧠 Key Concepts & Importance

- **Request Validation:** API Gateway can validate your request before it reaches the backend. This ensures that the backend only receives requests that meet your specific requirements (e.g., presence of headers, query parameters, or a specific body schema).
- **Edge Filtering:** Rejecting invalid requests at the edge (API Gateway) prevents unnecessary backend invocations (like Lambda or SQS), saving costs and reducing load on your infrastructure.
- **Request Validator:** A resource that defines what parts of the request to validate. In this lab, we validate the request parameters.
- **Method Configuration:** You specify which parameters are required at the method level. When paired with a validator, API Gateway enforces these rules.
- **400 Bad Request:** If a request fails validation, API Gateway automatically returns a 400 status code to the client, along with a descriptive error message.

## 🛠️ Command Reference

- `apigateway create-request-validator`: Creates a validator that can be applied to an API.
    - `--validate-request-parameters`: Enables validation of headers and query string parameters.
- `apigateway update-method`: Modifies the configuration of an existing method.
    - `--patch-operations`: Used to add requirements (like `userID`) and associate the validator ID.

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
