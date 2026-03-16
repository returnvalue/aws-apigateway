import boto3
import json

events = boto3.client('events', endpoint_url="http://localhost:4566", region_name="us-east-1")
iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
apigw = boto3.client('apigateway', endpoint_url="http://localhost:4566", region_name="us-east-1")

events.create_event_bus(Name='WebhookBus')

iam.put_role_policy(
    RoleName='ApiGatewayDirectRole',
    PolicyName='EventBridgeAccess',
    PolicyDocument=json.dumps({"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"events:PutEvents","Resource":"*"}]})
)

role = iam.get_role(RoleName='ApiGatewayDirectRole')
apigw_role = role['Role']['Arn']

apis = apigw.get_rest_apis()
api_id = next(api['id'] for api in apis.get('items', []) if api.get('name') == 'EnterpriseAPI')

resources = apigw.get_resources(restApiId=api_id)
parent_id = resources['items'][0]['id']

resource_response = apigw.create_resource(restApiId=api_id, parentId=parent_id, pathPart="events")
event_id = resource_response['id']

apigw.put_method(restApiId=api_id, resourceId=event_id, httpMethod='POST', authorizationType='NONE')

apigw.put_integration(
    restApiId=api_id,
    resourceId=event_id,
    httpMethod='POST',
    type='AWS',
    integrationHttpMethod='POST',
    uri="arn:aws:apigateway:us-east-1:events:action/PutEvents",
    credentials=apigw_role,
    requestParameters={'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"},
    requestTemplates={'application/json': 'Action=PutEvents&Version=2015-10-07&Event.1.Source=api.gateway&Event.1.EventBusName=WebhookBus&Event.1.DetailType=WebhookReceived&Event.1.Detail=$util.urlEncode($input.body)'}
)

apigw.put_method_response(restApiId=api_id, resourceId=event_id, httpMethod='POST', statusCode='200')
apigw.put_integration_response(restApiId=api_id, resourceId=event_id, httpMethod='POST', statusCode='200', selectionPattern="")
