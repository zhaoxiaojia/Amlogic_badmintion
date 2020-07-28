# encoding:utf-8
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from account.models import UserInfo
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown
import redis
from django.views import View
from django.conf import settings
from django.db.models import Count
from .models import ArticleColumn, ArticlePost, Comment, ArticleTag
from .forms import CommentForm, ArticleTagForm

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


# @method_decorator(login_required(), 'dispatch')
class ArticlePostTitleListView(ListView):
    model = ArticlePost
    template_name = 'article/list/article_title.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get(self, request, username=None):
        if username:
            user = User.objects.get(username=username)
            userinfo = UserInfo.objects.get(user_id=user.id)
            article_title = ArticlePost.objects.filter(author=user)
            return render(request, 'article/list/author_articles.html',
                          {'articles': article_title, 'userinfo': userinfo})
        else:
            article_title = ArticlePost.objects.all()
            return render(request, self.template_name, {'articles': article_title})


def article_detail(request, id, slug):
    context = {}
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    article.body = markdown.markdown(article.body.replace("\r\n", ' \n'), extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮拓展
        'markdown.extensions.toc'  # 自动生成目录
    ])
    context['article'] = article
    total_views = r.incr('article:{}:views'.format(article.id))
    r.zincrby('article_ranking', 1, article.id)  # 1
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]  # 2
    article_ranking_ids = [int(id) for id in article_ranking]
    article_tags_id = article.article_tag.values_list('id', flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_id).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('article_tag')).order_by('-same_tags', '-created')[:4]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))  # 3
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))  # 4
    context['total_views'] = total_views
    context['most_viewed'] = most_viewed
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
    context['comment_form'] = comment_form
    context['similar_articles'] = similar_articles
    return render(request, 'article/list/article_content.html', context)


@login_required()
@csrf_exempt
@require_POST
def like_article(request):
    article_id = request.POST.get('id')  # 1
    action = request.POST.get('action')  # 2
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == 'like':
                article.users_like.add(request.user)  # 3
                return HttpResponse('1')
            else:
                article.users_like.remove(request.user)  # 4
                return HttpResponse('2')
        except:
            return HttpResponse('no')
    else:
        return HttpResponse('3')
