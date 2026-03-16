import boto3

apigw = boto3.client('apigateway', endpoint_url="http://localhost:4566", region_name="us-east-1")

apis = apigw.get_rest_apis()
api_id = next(api['id'] for api in apis.get('items', []) if api.get('name') == 'EnterpriseAPI')

validator_response = apigw.create_request_validator(
    restApiId=api_id,
    name="RequireQueryString",
    validateRequestParameters=True
)
validator_id = validator_response['id']

resources = apigw.get_resources(restApiId=api_id)
sync_id = next(res['id'] for res in resources.get('items', []) if res.get('pathPart') == 'sync')

apigw.update_method(
    restApiId=api_id,
    resourceId=sync_id,
    httpMethod='GET',
    patchOperations=[
        {'op': 'add', 'path': '/requestParameters/method.request.querystring.userID', 'value': 'true'},
        {'op': 'replace', 'path': '/requestValidatorId', 'value': validator_id}
    ]
)
