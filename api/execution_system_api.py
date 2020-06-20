import functools
import logging

from rest_framework import serializers
from rest_framework import renderers

from api import apps, s3
from data_storage import models

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = (1, 60)

STATE_FINISHED = 'FINISHED'
STATE_FAILED = 'FAILED'
STATE_UNKNOWN_TASK = 'UNKNOWN_TASK'
STATE_SUCCESS = 'SUCCESS'
STATE_INITIALIZING = 'INITIALIZING'
STATE_RUNNING = 'RUNNING'
STATE_UNKNOWN = 'UNKNOWN'

SUCCESS_FINISH_STATES = (STATE_SUCCESS,)
WAITING_STATES = (STATE_INITIALIZING, STATE_RUNNING)
FAIL_STATES = (STATE_FINISHED, STATE_UNKNOWN_TASK, STATE_FAILED, STATE_UNKNOWN)

STATES = SUCCESS_FINISH_STATES + WAITING_STATES + FAIL_STATES

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


def s3_key_for_result(task_id):
    return 'result_' + task_id


def s3_key_for_metrics(task_id):
    return 'metrics_' + task_id


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
        ret['result'] = {
            's3_path': s3.generate_path(s3_key_for_result(ret['id'])),
            'metrics_s3_path':s3.generate_path(s3_key_for_metrics(ret['id'])),
        }
        if not ret['user_input']:
            ret.pop('user_input')
        return ret


class ModelTrainingTaskSerializer(serializers.ModelSerializer):
    model = NeuralModelSerializer()

    class Meta:
        model = models.TrainingTask
        fields = ['model', 'result_url']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['weights_url'] = ret.pop('result_url')
        ret.update(ret.pop('model'))
        return ret


class EvalTaskSerializer(serializers.ModelSerializer):
    train_task = ModelTrainingTaskSerializer()
    user_input = UserInputSerializer()

    class Meta:
        model = models.TrainingTask
        fields = ['id', 'parameters', 'train_task', 'user_input']

    def __init__(self, *args, **kwargs):
        self.task_type = kwargs.pop('task_type')
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = self.task_type
        ret['result'] = {'s3_path': s3.generate_path(s3_key_for_result(ret['id']))}
        ret['model'] = ret.pop('train_task')
        return ret


def start_task(task_id, task_data):
    result = apps.EXECUTION_SYSTEM_SESSION.post(apps.EXECUTION_SYSTEM_BASE_URL + f'/api/task/{task_id}/execute', data=task_data, timeout=REQUEST_TIMEOUT)
    result.raise_for_status()
    result_status = result.json()['result']
    if result_status not in ('SUCCESS', 'ALREADY_RUNNING'):
        raise ExecutionSystemError(f'Bad result {result_status}')


def start_learning_task(task):
    task_data = renderers.JSONRenderer().render(TrainingTaskSerializer(task, task_type=LEARNING).data)
    logger.info('start_learning_task %s', task_data)
    return start_task(task.id, task_data)


def start_applying_task(task):
    task_data = renderers.JSONRenderer().render(EvalTaskSerializer(task, task_type=APPLYING).data)
    logger.info('start_applying_task %s', task_data)
    return start_task(task.id, task_data)


def check_task(task, task_type=''):
    logger.info('check_{}_task %s'.format(task_type), task.id)
    try:
        result = apps.EXECUTION_SYSTEM_SESSION.get(apps.EXECUTION_SYSTEM_BASE_URL + f'/api/task/{task.id}/state', timeout=REQUEST_TIMEOUT)
        result.raise_for_status()
        state = result.json()['state']
        if state not in STATES:
            raise ExecutionSystemError(f'Unknown state {state}')
    except Exception:
        logger.warning('Check status failed', exc_info=True)
        return False
    if state in SUCCESS_FINISH_STATES:
        task.result_url = s3.generate_url(s3_key_for_result(task.id))
        task.status = models.TrainingTask.SUCCEEDED
        return True
    elif state in WAITING_STATES:
        return False
    elif state in FAIL_STATES:
        task.status = models.TrainingTask.FAILED
        task.error_message = 'Fail in execution system'
        return True
    else:
        task.status = models.TrainingTask.FAILED
        task.error_message = 'Unknown state in execution system'
        return True


check_learning_task = functools.partial(check_task, task_type=LEARNING)
check_applying_task = functools.partial(check_task, task_type=APPLYING)
