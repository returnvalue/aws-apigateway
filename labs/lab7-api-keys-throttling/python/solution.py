import boto3

apigw = boto3.client('apigateway', endpoint_url="http://localhost:4566", region_name="us-east-1")

apis = apigw.get_rest_apis()
api_id = next(api['id'] for api in apis.get('items', []) if api.get('name') == 'EnterpriseAPI')

resources = apigw.get_resources(restApiId=api_id)
sync_id = next(res['id'] for res in resources.get('items', []) if res.get('pathPart') == 'sync')

key_response = apigw.create_api_key(
    name="PremiumClientKey",
    enabled=True
)
key_id = key_response['id']

plan_response = apigw.create_usage_plan(
    name="PremiumTierPlan",
    apiStages=[{'apiId': api_id, 'stage': 'prod'}],
    throttle={'burstLimit': 10, 'rateLimit': 5},
    quota={'limit': 1000, 'offset': 0, 'period': 'MONTH'}
)
plan_id = plan_response['id']

apigw.create_usage_plan_key(
    usagePlanId=plan_id,
    keyId=key_id,
    keyType="API_KEY"
)

apigw.update_method(
    restApiId=api_id,
    resourceId=sync_id,
    httpMethod='GET',
    patchOperations=[
        {'op': 'replace', 'path': '/apiKeyRequired', 'value': 'true'}
    ]
)

apigw.create_deployment(
    restApiId=api_id,
    stageName='prod'
)
