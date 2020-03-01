import boto3

from django.apps import AppConfig
from django.conf import settings

from api import s3


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
