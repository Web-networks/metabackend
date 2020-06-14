import logging

from rest_framework import serializers
from rest_framework import renderers

from api import apps, s3
from data_storage import models

logger = logging.getLogger(__name__)

STATE_FINISHED = 'FINISHED'
STATE_FAILED = 'FAILED'
STATE_UNKNOWN_TASK = 'UNKNOWN_TASK'
STATE_SUCCESS = 'SUCCESS'
STATE_INITIALIZING = 'INITIALIZING'
STATE_RUNNING = 'RUNNING'
STATE_UNKNOWN = 'UNKNOWN'

STATES = (STATE_FINISHED, STATE_UNKNOWN_TASK, STATE_FAILED, STATE_SUCCESS, STATE_INITIALIZING, STATE_RUNNING, STATE_UNKNOWN)

LEARNING = 'learning'
APPLYING = 'applying'


class ExecutionSystemError(Exception):
    def __init__(self, message):
        super(ExecutionSystemError, self).__init__()
        self.message = message


class NeuralModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NeuralModel
        fields = ['id', 'execution_code_url']


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInput
        fields = ['id', 'data_url']


class TrainingTaskSerializer(serializers.ModelSerializer):
    model = NeuralModelSerializer()
    user_input = UserInputSerializer()

    class Meta:
        model = models.TrainingTask
        fields = ['id', 'parameters', 'model', 'user_input']

    def __init__(self, *args, **kwargs):
        self.task_type = kwargs.pop('task_type')
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = self.task_type
        ret['result'] = {'s3_path': s3.generate_path('result_' + ret['id'])}
        return ret


def start_learning_task(task):
    task_data = renderers.JSONRenderer().render(TrainingTaskSerializer(task, task_type=LEARNING).data)
    logger.info('start_learning_task %s', task_data)
    result = apps.EXECUTION_SYSTEM_SESSION.post(apps.EXECUTION_SYSTEM_BASE_URL + f'/api/task/{task.id}/execute', data=task_data)
    result.raise_for_status()
    result_status = result.json()['result']
    if result_status not in ('SUCCESS', 'ALREADY_RUNNING'):
        raise ExecutionSystemError(f'Bad result {result_status}')


def check_learning_task(task):
    logger.info('check_learning_task %s', task.id)
    try:
        result = apps.EXECUTION_SYSTEM_SESSION.get(apps.EXECUTION_SYSTEM_BASE_URL + f'/api/task/{task.id}/state')
        result.raise_for_status()
        state = result.json()['state']
        if state not in STATES:
            raise ExecutionSystemError(f'Unknown state {state}')
    except Exception:
        logger.warning('Check status failed', exc_info=True)
        return False
    if state in (STATE_FINISHED, STATE_SUCCESS):
        task.status = models.TrainingTask.SUCCEEDED
        return True
    elif state in (STATE_UNKNOWN, STATE_FINISHED, STATE_UNKNOWN_TASK):
        task.status = models.TrainingTask.FAILED
        task.error_message = 'Unknown state in execution system'
        return True
    return False
