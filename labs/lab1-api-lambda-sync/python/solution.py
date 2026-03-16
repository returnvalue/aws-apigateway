import boto3
import json
import zipfile
import os

iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
lambda_client = boto3.client('lambda', endpoint_url="http://localhost:4566", region_name="us-east-1")
apigw = boto3.client('apigateway', endpoint_url="http://localhost:4566", region_name="us-east-1")

with open('api_handler.py', 'w') as f:
    f.write('import json\ndef lambda_handler(event, context):\n    return {"statusCode": 200, "body": json.dumps({"message": "Synchronous response from Lambda!"})}\n')

with zipfile.ZipFile('function.zip', 'w') as z:
    z.write('api_handler.py')

role_response = iam.create_role(
    RoleName='APILambdaRole',
    AssumeRolePolicyDocument=json.dumps({"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]})
)
role_arn = role_response['Role']['Arn']

with open('function.zip', 'rb') as f:
    zip_bytes = f.read()

lambda_response = lambda_client.create_function(
    FunctionName='ApiCompute',
    Runtime='python3.9',
    Role=role_arn,
    Handler='api_handler.lambda_handler',
    Code={'ZipFile': zip_bytes}
)
lambda_arn = lambda_response['FunctionArn']

api_response = apigw.create_rest_api(name="EnterpriseAPI")
api_id = api_response['id']

resources = apigw.get_resources(restApiId=api_id)
parent_id = resources['items'][0]['id']

resource_response = apigw.create_resource(restApiId=api_id, parentId=parent_id, pathPart="sync")
sync_id = resource_response['id']

apigw.put_method(restApiId=api_id, resourceId=sync_id, httpMethod='GET', authorizationType='NONE')

apigw.put_integration(
    restApiId=api_id,
    resourceId=sync_id,
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
)
