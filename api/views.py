import uuid

from data_storage import models
from django.http import JsonResponse

from api import s3


def generate_code(model_schema):
    return 'BEST CODE EVER'


def create_model(request):
    user_id = request.headers['x-user-id']
    assert user_id
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
