import boto3

apigw = boto3.client('apigateway', endpoint_url="http://localhost:4566", region_name="us-east-1")

apis = apigw.get_rest_apis()
api_id = next(api['id'] for api in apis.get('items', []) if api.get('name') == 'EnterpriseAPI')

apigw.create_deployment(
    restApiId=api_id,
    stageName='dev',
    description='Initial Development Deployment'
)

apigw.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='Production Release'
)
