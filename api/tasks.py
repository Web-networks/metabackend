import logging

from celery import shared_task

from data_storage import models

logger = logging.getLogger(__name__)


class NotReadyException(Exception):
    pass


@shared_task(default_retry_delay=15, autoretry_for=(NotReadyException,))
def wait_train_task(task_id):
    logger.info('Wait train task %s', task_id)
    task = models.TrainingTask.objects.get(pk=task_id)
    if task.status == models.TrainingTask.INITIAL:
        task.status = models.TrainingTask.WAITING
        task.save()
        raise NotReadyException()
