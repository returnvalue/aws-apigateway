import boto3
import json

sns = boto3.client('sns', endpoint_url="http://localhost:4566", region_name="us-east-1")
iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
apigw = boto3.client('apigateway', endpoint_url="http://localhost:4566", region_name="us-east-1")

topic_response = sns.create_topic(Name='BroadcastTopic')
topic_arn = topic_response['TopicArn']

iam.put_role_policy(
    RoleName='ApiGatewayDirectRole',
    PolicyName='SNSAccess',
    PolicyDocument=json.dumps({"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"sns:Publish","Resource":"*"}]})
)

role = iam.get_role(RoleName='ApiGatewayDirectRole')
apigw_role = role['Role']['Arn']

apis = apigw.get_rest_apis()
api_id = next(api['id'] for api in apis.get('items', []) if api.get('name') == 'EnterpriseAPI')

resources = apigw.get_resources(restApiId=api_id)
parent_id = resources['items'][0]['id']

resource_response = apigw.create_resource(restApiId=api_id, parentId=parent_id, pathPart="broadcast")
broadcast_id = resource_response['id']

apigw.put_method(restApiId=api_id, resourceId=broadcast_id, httpMethod='POST', authorizationType='NONE')

apigw.put_integration(
    restApiId=api_id,
    resourceId=broadcast_id,
    httpMethod='POST',
    type='AWS',
    integrationHttpMethod='POST',
    uri="arn:aws:apigateway:us-east-1:sns:action/Publish",
    credentials=apigw_role,
    requestParameters={'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"},
    requestTemplates={'application/json': f"Action=Publish&TopicArn=$util.urlEncode('{topic_arn}')&Message=$util.urlEncode($input.body)"}
)

apigw.put_method_response(restApiId=api_id, resourceId=broadcast_id, httpMethod='POST', statusCode='200')
apigw.put_integration_response(restApiId=api_id, resourceId=broadcast_id, httpMethod='POST', statusCode='200', selectionPattern="")
