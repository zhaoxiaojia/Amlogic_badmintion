from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.html import mark_safe
from mdeditor.fields import MDTextField


# Create your models here.

class ArticleColumn(models.Model):
    '''
    auto_now:无论你是添加还是修改对象，时间为你添加或者修改的时间，相当于更新时间。
    auto_now_add:添加时的时间，更新对象时不会有变动，相当于给时间做了一次定位。
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_column')
    column = models.CharField(max_length=200, verbose_name='标题')
    created = models.DateField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.column

    class Meta:
        db_table = 'user_article'
        verbose_name = '栏目'
        verbose_name_plural = verbose_name


class ArticleTag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tag')
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')
    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.CharField(max_length=500, verbose_name='网络标题')
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name='article_column',
                               verbose_name='栏目')
    body = MDTextField(verbose_name='内容')
    created = models.DateTimeField(default=timezone.now(), verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    users_like = models.ManyToManyField(User, related_name='articles_like', blank=True)

    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)

    class Meta():
        db_table = 'user_post'
        ordering = ('-updated',)
        verbose_name = verbose_name_plural = '帖子'
        index_together = (('id', 'slug'))  # 3 建立索引

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # 4
        self.slug = slugify(self.title)  # 5
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):  # 6
        # 获取文章对象的url
        return reverse('article:article_detail', args=[self.id, self.slug])

    def get_url_path(self):
        return reverse('article:article_content', args=[self.id, self.slug])


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {} '.format(self.commentator.username, self.article)
