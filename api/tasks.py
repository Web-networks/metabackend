import logging
import traceback

from celery import shared_task, exceptions

from data_storage import models
from api import execution_system_api

logger = logging.getLogger(__name__)


def process_exception(e):
    if isinstance(e, exceptions.CeleryError):
        raise


def fail_task(task):
    logger.exception('Task FAILED')
    task.status = models.TrainingTask.FAILED
    task.error_message = traceback.format_exc(limit=4096)[-1024:]
    task.save()


@shared_task()
def init_train_task(task_id):
    logger.info('Init train task %s', task_id)
    task = models.TrainingTask.objects.get(pk=task_id)
    try:
        assert task.status == models.TrainingTask.INITIAL
        execution_system_api.start_learning_task(task)
    except Exception as e:
        process_exception(e)
        fail_task(task)
    else:
        task.status = models.TrainingTask.WAITING
        task.save()
        wait_train_task.apply_async(args=(task.id,), countdown=60)


@shared_task()
def wait_train_task(task_id):
    logger.info('Wait train task %s', task_id)
    task = models.TrainingTask.objects.get(pk=task_id)
    try:
        assert task.status == models.TrainingTask.WAITING
        is_finished = execution_system_api.check_learning_task(task)
        task.save()
        if not is_finished:
            wait_train_task.apply_async(args=(task.id,), countdown=60)
    except Exception as e:
        process_exception(e)
        fail_task(task)
