# Generated by Django 3.0.8 on 2020-07-18 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_userinfo_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='stage',
            field=models.IntegerField(choices=[(1, '参赛'), (2, '未参赛'), (0, '待定')], default=0, verbose_name='参赛状态'),
        ),
    ]
