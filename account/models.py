from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserInfo(models.Model):
    SEX_ITEMS = [
        (1, '男'),
        (2, '女'),
        (0, '未知')
    ]
    RANK_STAGE = [
        (1, '参赛'),
        (2, '未参赛'),
        (0, '待定'),
    ]
    name = models.CharField(max_length=300, verbose_name='选手', default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, verbose_name='帐号')
    sex = models.IntegerField(choices=SEX_ITEMS, verbose_name='性别')
    depart = models.CharField(max_length=100, blank=True, verbose_name='部门')
    phone = models.CharField(max_length=100, blank=True, verbose_name='手机号')
    station = models.CharField(max_length=100, blank=True, verbose_name='工位')
    photo = models.ImageField(blank=True, verbose_name='照片', upload_to='photos')
    rank = models.CharField(max_length=100, blank=True, verbose_name='比赛排名')
    stage = models.IntegerField(choices=RANK_STAGE, blank=True, verbose_name='参赛状态')

    def __str__(self):
        return '选手：{}'.format(self.user.username)

    @property
    def image_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    class Meta:
        db_table = 'badminton_user'
        verbose_name = '选手信息'
        verbose_name_plural = verbose_name
