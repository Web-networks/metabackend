import logging
import traceback

from celery import shared_task

from data_storage import models
from api import execution_system_api

logger = logging.getLogger(__name__)


class NotReadyException(Exception):
    pass


@shared_task(default_retry_delay=60, autoretry_for=(NotReadyException,))
def wait_train_task(task_id):
    logger.info('Wait train task %s', task_id)
    task = models.TrainingTask.objects.get(pk=task_id)
    if task.status == models.TrainingTask.INITIAL:
        try:
            execution_system_api.start_learning_task(task)
        except Exception:
            task.status = models.TrainingTask.FAILED
            task.error_message = traceback.format_exc(limit=4096)
            task.save()
        else:
            task.status = models.TrainingTask.WAITING
            task.save()
            raise NotReadyException()
    elif task.status == models.TrainingTask.WAITING:
        is_finished = execution_system_api.check_learning_task(task)
        task.save()
        if not is_finished:
            raise NotReadyException()
