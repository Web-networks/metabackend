import functools
import json
import logging
import uuid

from django.http import JsonResponse
from django.db.transaction import on_commit

from data_storage import models

from api import s3
from api import tasks as celery_tasks

logger = logging.getLogger(__name__)


class ClientError(ValueError):
    def __init__(self, error_message):
        self.message = error_message


class ValidationError(ClientError):
    status_code = 400


class PermissionError(ClientError):
    status_code = 403


def catch_client_error(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientError as e:
            return JsonResponse({'error': e.message}, status=e.status_code)

    return wrapped


def get_user_id(request):
    try:
        user_id = request.headers['x-user-id']
        assert user_id
    except (AssertionError, KeyError):
        raise ValidationError('Bad user id')
    return user_id


def generate_code(model_schema):
    return 'BEST CODE EVER'


@catch_client_error
def create_model(request):
    user_id = get_user_id(request)
    code = generate_code(request.body)
    model_id = str(uuid.uuid4())
    s3_key = 'model_' + model_id
    s3.upload_object(s3_key, code)
    model = models.NeuralModel(
        id=model_id,
        user_id=user_id,
        execution_code_url=s3.generate_url(s3_key),
    )

    model.save()
    return JsonResponse({'model_id': model.id})


class StartTrainTaskRequest(object):
    __slots__ = ('model_id', 'user_input_id', 'parameters')

    def __init__(self, model_id, user_input_id, parameters):
        self.model_id = model_id
        self.user_input_id = user_input_id
        self.parameters = parameters

    @classmethod
    def parse_from_body(cls, body):
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            logger.exception('Can\'t parse body')
            raise ValidationError('Bad json body')
        return cls(*(parsed[field] for field in cls.__slots__))


@catch_client_error
def start_train_task(request):
    user_id = get_user_id(request)
    parsed_request = StartTrainTaskRequest.parse_from_body(request.body)

    model = models.NeuralModel.objects.get(pk=parsed_request.model_id)
    if model.user_id != user_id:
        raise PermissionError('Permission to model denied')
    user_input = models.UserInput.objects.get(pk=parsed_request.user_input_id)
    if user_input.user_id != user_id:
        raise PermissionError('Permission to user_input denied')

    task = models.TrainingTask(
        id=str(uuid.uuid4()),
        user_id=user_id,
        model=model,
        user_input=user_input,
        parameters=parsed_request.parameters,
        status=models.TrainingTask.INITIAL,
        error_message='',
        result_url=''
    )

    task.save()
    on_commit(lambda: celery_tasks.wait_train_task.apply_async(args=(task.id,)))
    return JsonResponse({'task_id': task.id})


@catch_client_error
def upload_user_input(request):
    user_id = get_user_id(request)
    user_input_id = str(uuid.uuid4())
    s3_key = 'user_input_' + user_input_id
    s3.upload_multipart_data(s3_key, request.FILES['file'])

    user_input = models.UserInput(
        id=user_input_id,
        user_id=user_id,
        data_url=s3.generate_url(s3_key),
    )

    user_input.save()
    return JsonResponse({'user_input_id': user_input.id})
