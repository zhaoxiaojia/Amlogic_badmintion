# Generated by Django 3.0.8 on 2020-07-12 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200711_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.CharField(default='', max_length=300, verbose_name='邮箱'),
        ),
    ]
