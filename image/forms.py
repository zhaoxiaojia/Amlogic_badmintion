# encoding:utf-8
from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description')

    def clean_url(self):  # 10
        # 判断请求时否为图片类型
        url = self.cleaned_data['url']  # 11
        valid_extensions = ['jpg', 'jpeg', 'png']  # 12
        extension = url.rsplit('.', 1)[1].lower()  # 13 获取文件的后缀类型
        if extension not in valid_extensions:  # 14 判断是否时图片类型
            raise forms.ValidationError('请求非图片')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):  # 16
        print('save')
        image = super(ImageForm, self).save(commit=False)  # 17
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
        print(image_name)
        response = request.urlopen(image_url)  # 18
        print(response)
        image.image.save(image_name, ContentFile(response.read()), save=False)  # 19
        if commit:
            image.save()

        return image
