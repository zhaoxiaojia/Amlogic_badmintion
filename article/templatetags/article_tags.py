# encoding:utf-8
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
from article.models import ArticlePost


@register.simple_tag()
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag()
def author_total_articles(userinfo):
    return ArticlePost.objects.filter(author_id=userinfo.user_id).count()


@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by('-created')[:n]
    return {'latest_articles': latest_articles}


@register.simple_tag()  # 1
def most_commented_articles(n=3):  #
    return ArticlePost.objects.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:n]  # annotate 将从comment 表中查出来的数量标注在对应文章数据上


@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))
