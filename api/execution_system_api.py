import logging

from rest_framework import serializers

from api import apps
from data_storage import models

logger = logging.getLogger(__name__)

STATE_FINISHED = "FINISHED"
STATE_RUNNING = "RUNNING"
STATE_UNKNOWN = "UNKNOWN"

STATES = (STATE_FINISHED, STATE_RUNNING, STATE_UNKNOWN)


class ExecutionSystemError(Exception):
    def __init__(self, message):
        super(ExecutionSystemError, self).__init__()
        self.message = message


class TrainingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrainingTask
        fields = '__all__'


def start_learning_task(task):
    task_data = TrainingTaskSerializer(task).data
    logger.info('start_learning_task %s', task_data)
    result = apps.EXECUTION_SYSTEM_SESSION.post(apps.EXECUTION_SYSTEM_BASE_URL + f'/api/task/{task.id}/execute', json=task_data)
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
    except:
        logger.warning('Check status failed', exc_info=True)
        return False
    if state == STATE_FINISHED:
        task.status = models.TrainingTask.SUCCEEDED
        return True
    elif state == STATE_UNKNOWN:
        task.status = models.TrainingTask.FAILED
        task.error_message = 'Unknown state in execution system'
        return True
    return False
