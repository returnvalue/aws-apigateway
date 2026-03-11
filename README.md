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
* **Deployment Management:** managing immutable snapshots and Stages (dev/prod) for CI/CD.
* **API Security:** (Upcoming) Implementing API Keys and Usage Plans for throttling.

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
> **Session Persistence:** These labs rely on bash variables (like `$API_ID`, `$LAMBDA_ARN`, `$VALIDATOR_ID`, etc.). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Foundational API & Synchronous Lambda](./labs/lab1-api-lambda-sync/README.md)
2. [Lab 2: Storage-First Pattern (Direct SQS Integration)](./labs/lab2-api-sqs-async/README.md)
3. [Lab 3: Fan-Out Webhooks (Direct SNS Integration)](./labs/lab3-api-sns-fanout/README.md)
4. [Lab 4: Event Routing (Direct EventBridge Integration)](./labs/lab4-api-eventbridge/README.md)
5. [Lab 5: Payload Edge Validation](./labs/lab5-api-validation/README.md)
6. [Lab 6: API Deployments & Stages](./labs/lab6-api-deployments/README.md)
