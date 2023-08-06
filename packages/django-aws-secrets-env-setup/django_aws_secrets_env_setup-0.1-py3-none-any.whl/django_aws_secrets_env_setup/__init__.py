import boto3
import os
import base64
import json


def __get_secrets(secret_name, default_region_name, **kwargs):
    try:
        region_name = os.environ["SECRETS_REGION_NAME"]
    except:
        region_name = default_region_name

    session = boto3.session.Session()
    try:
        client = session.client(
            service_name=kwargs.get('service_name', 'secretsmanager'),
            region_name=region_name
        )
    except:
        client = session.client(
            service_name=kwargs.get('service_name', 'secretsmanager'),
            region_name=region_name,
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    if 'SecretString' in get_secret_value_response:
        secrets = get_secret_value_response['SecretString']
    else:
        secrets = base64.b64decode(get_secret_value_response['SecretBinary'])
    return json.loads(secrets)


def set_env_variables(secret_name, default_region_name, **kwargs):
    try:
        secrets = __get_secrets(secret_name, default_region_name, **kwargs)

        for k,v in secrets.items():
            os.environ[k] = str(v)
    except:
        pass