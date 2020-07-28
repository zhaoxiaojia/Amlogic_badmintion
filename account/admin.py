# encoding:utf-8
from django.contrib import admin
from .models import UserInfo


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'sex', 'depart', 'preview', 'station', 'photo', 'rank', 'stage')
    list_filter = ('sex',)

    def preview(self, obj):
        return obj.photo
