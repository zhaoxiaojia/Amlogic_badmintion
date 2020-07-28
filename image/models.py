from django.db import models
from django.contrib.auth.models import User

from slugify import slugify


# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=300)
    # url = models.URLField()
    slug = models.SlugField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)    # db_index 设置该属性 作为索引
    image = models.ImageField(upload_to='image/%Y/%m/%d')

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
