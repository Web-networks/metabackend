import boto3
import requests
import requests.adapters

from django.apps import AppConfig
from django.conf import settings

from api import s3

EXECUTION_SYSTEM_BASE_URL = ''
EXECUTION_SYSTEM_SESSION = requests.Session()


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        session = boto3.session.Session()
        s3.S3 = session.client(
            service_name='s3',
            config=boto3.session.Config(**settings.S3_CONFIG),
            **settings.S3_CREDENTIALS,
        )

        s3.S3_ENDPOINT = settings.S3_ENDPOINT
        s3.S3_BUCKET = settings.S3_BUCKET

        execution_system_session = requests.Session()
        execution_system_session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))

        global EXECUTION_SYSTEM_SESSION
        EXECUTION_SYSTEM_SESSION = execution_system_session
        global EXECUTION_SYSTEM_BASE_URL
        EXECUTION_SYSTEM_BASE_URL = settings.EXECUTION_SYSTEM_BASE_URL
