# encoding:utf-8
from django.urls import path, re_path
from django.conf.urls import url

from . import views, list_views
from .views import ArticleColumnListView, ArticleColumnView, ArticlePostView, ArticlePostListView, ArticleTagView
from .list_views import ArticlePostTitleListView

urlpatterns = [
    url(r'^article_column/$', ArticleColumnView.as_view(), name='article_column'),
    url(r'^rename_column/$', views.rename_article_column, name='rename_article_column'),
    url(r'^del_column/$', views.del_article_column, name='del_article_column'),
    url(r'^del_article/$', views.del_article, name='del_article'),
    url(r'^article_post/$', ArticlePostView.as_view(), name='article_post'),
    url(r'^article_list/$', ArticlePostListView.as_view(), name='article_list'),
    url(r'^article_title/$', ArticlePostTitleListView.as_view(), name='article_title'),
    path(r'^article_title/<username>/$', ArticlePostTitleListView.as_view(), name='author_articles'),
    url(r'^redit_article/(?P<article_id>\d+)/$', views.redit_article, name='redit_article'),
    url(r'^like_article/$', list_views.like_article, name='like_article'),
    re_path(r'^article_detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.article_detail, name="article_detail"),
    re_path(r'^article_content/(?P<id>\d+)/(?P<slug>[-\w]+)/$', list_views.article_detail, name="article_content"),
    url(r'^article_tag/$', ArticleTagView.as_view(), name='article_tag'),
    url(r'^del_article_tag/$', views.del_article_tag, name='del_article_tag'),
]
