# Generated by Django 3.0.3 on 2020-06-20 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_storage', '0003_evaltask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingtask',
            name='user_input',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='data_storage.UserInput'),
        ),
    ]
