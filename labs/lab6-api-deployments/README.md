# Lab 6: API Deployments & Stages

**Goal:** API changes in AWS do not go live automatically. You must bundle your resources, methods, and integrations into a Deployment and attach it to a Stage (e.g., `dev`, `v1`, `prod`) to make them accessible via a URL.
```bash
# 1. Deploy the current state of the API to a 'dev' stage
awslocal apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name dev \
  --description "Initial Development Deployment"
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name dev \
  --description "Initial Development Deployment"

# 2. Deploy the same state to a 'prod' stage
awslocal apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod \
  --description "Production Release"
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod \
  --description "Production Release"
```

## 🧠 Key Concepts & Importance

- **API Deployment:** A point-in-time snapshot of your API's resources and methods. For your changes to take effect, you must create a new deployment.
- **API Stage:** A logical reference to a deployment. Stages allow you to manage multiple versions of your API simultaneously (e.g., `/dev` for testing and `/prod` for live traffic).
- **Environment Isolation:** Stages allow you to use different backend integrations or environment variables (using Stage Variables) for different environments without changing the API structure.
- **Immutable Snapshots:** Deployments are immutable. If you change a resource but don't redeploy, the existing stage URL will still serve the old configuration.
- **Invocation URLs:** The base URL for your API includes the stage name (e.g., `https://{api-id}.execute-api.{region}.amazonaws.com/{stage-name}/`).

## 🛠️ Command Reference

- `apigateway create-deployment`: Creates a deployment resource, which makes the API accessible to clients.
    - `--rest-api-id`: The string identifier of the associated RestApi.
    - `--stage-name`: The name of the stage for the deployment.
    - `--description`: A brief description of the deployment.

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
