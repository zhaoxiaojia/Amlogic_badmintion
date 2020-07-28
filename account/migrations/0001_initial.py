# Generated by Django 3.0.8 on 2020-07-11 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女'), (0, '未知')], verbose_name='性别')),
                ('depart', models.CharField(blank=True, max_length=100, verbose_name='部门')),
                ('phone', models.CharField(blank=True, max_length=100, verbose_name='手机号')),
                ('station', models.CharField(blank=True, max_length=100, verbose_name='工位')),
                ('photo', models.ImageField(blank=True, upload_to='', verbose_name='照片')),
                ('rank', models.CharField(blank=True, max_length=100, verbose_name='比赛排名')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='姓名')),
            ],
            options={
                'verbose_name': '选手信息',
                'verbose_name_plural': '选手信息',
                'db_table': 'badminton_user',
            },
        ),
    ]
