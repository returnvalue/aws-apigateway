import boto3
import json

sts = boto3.client('sts', endpoint_url="http://localhost:4566", region_name="us-east-1")
sqs = boto3.client('sqs', endpoint_url="http://localhost:4566", region_name="us-east-1")
iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
apigw = boto3.client('apigateway', endpoint_url="http://localhost:4566", region_name="us-east-1")

account_id = sts.get_caller_identity()['Account']
sqs.create_queue(QueueName='IngestionQueue')

role_response = iam.create_role(
    RoleName='ApiGatewayDirectRole',
    AssumeRolePolicyDocument=json.dumps({"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"apigateway.amazonaws.com"},"Action":"sts:AssumeRole"}]})
)
apigw_role = role_response['Role']['Arn']

iam.put_role_policy(
    RoleName='ApiGatewayDirectRole',
    PolicyName='SQSAccess',
    PolicyDocument=json.dumps({"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"sqs:SendMessage","Resource":"*"}]})
)

apis = apigw.get_rest_apis()
api_id = next(api['id'] for api in apis.get('items', []) if api.get('name') == 'EnterpriseAPI')

resources = apigw.get_resources(restApiId=api_id)
parent_id = resources['items'][0]['id']

resource_response = apigw.create_resource(restApiId=api_id, parentId=parent_id, pathPart="async")
async_id = resource_response['id']

apigw.put_method(restApiId=api_id, resourceId=async_id, httpMethod='POST', authorizationType='NONE')

apigw.put_integration(
    restApiId=api_id,
    resourceId=async_id,
    httpMethod='POST',
    type='AWS',
    integrationHttpMethod='POST',
    uri=f"arn:aws:apigateway:us-east-1:sqs:path/{account_id}/IngestionQueue",
    credentials=apigw_role,
    requestParameters={'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"},
    requestTemplates={'application/json': 'Action=SendMessage&MessageBody=$util.urlEncode($input.body)'}
)

apigw.put_method_response(restApiId=api_id, resourceId=async_id, httpMethod='POST', statusCode='200')
apigw.put_integration_response(restApiId=api_id, resourceId=async_id, httpMethod='POST', statusCode='200', selectionPattern="")
