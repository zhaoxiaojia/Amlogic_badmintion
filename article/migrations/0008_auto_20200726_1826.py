# Generated by Django 3.0.8 on 2020-07-26 10:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20200726_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 10, 26, 51, 79699, tzinfo=utc), verbose_name='创建时间'),
        ),
    ]