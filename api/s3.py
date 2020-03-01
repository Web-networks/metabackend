S3 = None
S3_ENDPOINT = None
S3_BUCKET = None


def upload_object(key, data):
    S3.put_object(Bucket=S3_BUCKET, Key=key, Body=data)


def generate_url(key):
    return '/'.join((S3_ENDPOINT, S3_BUCKET, key))
