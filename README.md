# AWS API Gateway Serverless Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-API_Gateway-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon API Gateway concepts, from RESTful API design and Lambda integrations to asynchronous patterns, security, and deployment stages. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS API management environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Synchronous REST APIs:** Connecting HTTP endpoints to Lambda functions via Proxy Integrations.
* **Asynchronous Processing:** Implementing the Storage-First pattern using direct SQS integrations.
* **Fan-Out Webhooks:** Integrating directly with SNS to broadcast messages to multiple subscribers.
* **Event Routing:** Directly ingesting webhooks onto an EventBridge Custom Bus.
* **Request Validation:** Enforcing parameter and schema validation at the edge to reduce backend load.
* **Deployment Management:** Managing immutable snapshots and Stages (dev/prod) for CI/CD.
* **API Security:** Implementing API Keys and Usage Plans for throttling and monetization.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   
```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   
```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving API infrastructure.
>
> **Session Persistence:** These labs rely on bash variables (like `$API_ID`, `$LAMBDA_ARN`, `$VALIDATOR_ID`, `$PLAN_ID`, etc.). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Foundational API & Synchronous Lambda](./labs/lab1-api-lambda-sync/README.md)
2. [Lab 2: Storage-First Pattern (Direct SQS Integration)](./labs/lab2-api-sqs-async/README.md)
3. [Lab 3: Fan-Out Webhooks (Direct SNS Integration)](./labs/lab3-api-sns-fanout/README.md)
4. [Lab 4: Event Routing (Direct EventBridge Integration)](./labs/lab4-api-eventbridge/README.md)
5. [Lab 5: Payload Edge Validation](./labs/lab5-api-validation/README.md)
6. [Lab 6: API Deployments & Stages](./labs/lab6-api-deployments/README.md)
7. [Lab 7: Monetization & Security (API Keys & Throttling)](./labs/lab7-api-keys-throttling/README.md)

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
