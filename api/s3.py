from botocore.exceptions import ClientError
import logging

from api import apps

logger = logging.getLogger(__name__)


def get_object(key):
    result_object = apps.S3_RESOURCE.Object(apps.S3_BUCKET, key)
    try:
        response = result_object.get()
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return None
        else:
            raise

    if response.get('DeleteMarker', False):
        return None
    return response['Body'].read()


def upload_object(key, data):
    result_object = apps.S3_RESOURCE.Object(apps.S3_BUCKET, key)
    result_object.put(Body=data)


def generate_url(key):
    return '/'.join((apps.S3_ENDPOINT, apps.S3_BUCKET, key))


def generate_path(key):
    return '/'.join(('s3:/', apps.S3_BUCKET, key))


def combine_chunks(chunks, recommended_size=50 * 1024 * 1024):
    big_chunk = list()
    current_size = 0
    for chunk in chunks:
        current_size += len(chunk)
        big_chunk.append(chunk)
        if current_size >= recommended_size:
            yield b''.join(big_chunk)
            big_chunk = list()
            current_size = 0
    if current_size > 0:
        yield b''.join(big_chunk)


def upload_multipart_data(key, file):
    result_object = apps.S3_RESOURCE.Object(apps.S3_BUCKET, key)
    multipart_upload = result_object.initiate_multipart_upload()
    try:
        parts = list()
        for i, chunk in enumerate(combine_chunks(file.chunks())):
            part_number = i + 1
            part = multipart_upload.Part(part_number)
            logger.info('Part size: %s', len(chunk))
            response = part.upload(Body=chunk)
            logger.info('Successfully upload %s part, tag: %s', part_number, response['ETag'])
            parts.append({
                'PartNumber': part_number,
                'ETag': response['ETag'],
            })
        multipart_upload.complete(MultipartUpload={'Parts': parts})
    except Exception:
        logger.warning('Abort multipart upload')
        multipart_upload.abort()
        raise
