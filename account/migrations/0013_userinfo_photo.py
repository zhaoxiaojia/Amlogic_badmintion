# Generated by Django 3.0.8 on 2020-07-19 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_userinfo_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(blank=True, upload_to='', verbose_name='照片'),
        ),
    ]
