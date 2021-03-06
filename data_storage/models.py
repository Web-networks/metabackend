from django.db import models


# Create your models here.


class NeuralModel(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    user_id = models.CharField(max_length=30)
    execution_code_url = models.URLField()


class UserInput(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    user_id = models.CharField(max_length=30)
    data_url = models.URLField()


class Task(object):
    INITIAL = 'INITIAL'
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    REJECTED = 'REJECTED'
    FAILED = 'FAILED'
    SUCCEEDED = 'SUCCEEDED'

    STATUS_CHOICES = [
        (INITIAL, 'Initial'),
        (WAITING, 'Waiting'),
        (RUNNING, 'Running'),
        (REJECTED, 'Rejected'),
        (FAILED, 'Failed'),
        (SUCCEEDED, 'Succeeded'),
    ]


class TrainingTask(models.Model, Task):
    id = models.CharField(primary_key=True, max_length=40)
    user_id = models.CharField(max_length=30, editable=False)

    model = models.ForeignKey(
        NeuralModel,
        models.PROTECT,
        editable=False,
    )
    user_input = models.ForeignKey(
        UserInput,
        models.PROTECT,
        editable=False,
        blank=True,
        null=True,
    )
    parameters = models.CharField(
        help_text='Parameters in json',
        max_length=4096,
        editable=False,
    )

    status = models.CharField(max_length=30, choices=Task.STATUS_CHOICES)
    error_message = models.CharField(max_length=1024, blank=True)
    result_url = models.URLField(blank=True)
    metrics = models.CharField(max_length=8 * 1024, blank=True)


class EvalTask(models.Model, Task):
    id = models.CharField(primary_key=True, max_length=40)
    user_id = models.CharField(max_length=30, editable=False)

    train_task = models.ForeignKey(
        TrainingTask,
        models.PROTECT,
        editable=False,
    )
    user_input = models.ForeignKey(
        UserInput,
        models.PROTECT,
        editable=False,
    )
    parameters = models.CharField(
        help_text='Parameters in json',
        max_length=4096,
        editable=False,
    )

    status = models.CharField(max_length=30, choices=Task.STATUS_CHOICES)
    error_message = models.CharField(max_length=1024, blank=True)
    result = models.CharField(max_length=8 * 1024, blank=True)
