# Lab 6: API Deployments & Stages

**Goal:** API changes in AWS do not go live automatically. You must bundle your resources, methods, and integrations into a Deployment and attach it to a Stage (e.g., `dev`, `v1`, `prod`) to make them accessible via a URL.

```bash
# 1. Deploy the current state of the API to a 'dev' stage
awslocal apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name dev \
  --description "Initial Development Deployment"

# 2. Deploy the same state to a 'prod' stage
awslocal apigateway create-deployment \
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
