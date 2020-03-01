import boto3
import json

with open('../../yandex-credentials.json') as credentials:
    credentials = json.load(credentials)

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    **credentials
)

bucket_name = 'code-testing'
object_key = 'test'
## Из строки
s3.put_object(Bucket=bucket_name, Key=object_key, Body='TEST_BODY')

# Получить список объектов в бакете
for key in s3.list_objects(Bucket=bucket_name)['Contents']:
    print(key['Key'])

# Получить объект
get_object_response = s3.get_object(Bucket=bucket_name, Key=object_key)
print(get_object_response['Body'].read())
