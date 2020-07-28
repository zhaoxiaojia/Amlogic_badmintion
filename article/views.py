from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import markdown
import json

from .models import ArticleColumn, ArticlePost, ArticleTag
from .forms import ArticleColumnForm, ArticlePostForm, ArticleTagForm

ITEMS_PER_PAGE = 2


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ArticleColumnListView(ListView):
    # 展示帖子
    model = ArticleColumn
    context_object_name = 'columns'
    template_name = 'article/column/article_column.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ArticleColumnView(View):
    def get(self, request):
        columns = ArticleColumn.objects.filter()
        column_form = ArticleColumnForm()
        return render(request, 'article/column/article_column.html', {'columns': columns, 'column_form': column_form})

    def post(self, request):
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)  # 7
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse('1')


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ArticlePostView(View):
    def get(self, request):
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request, 'article/column/article_post.html', {
            'article_post_form': article_post_form,
            'article_columns': article_columns,
            'article_tags': article_tags,
        })

    def post(self, request):
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse('1')
            except:
                return HttpResponse('2')

        else:
            return HttpResponse('3')


@method_decorator(login_required(), 'dispatch')
class ArticlePostListView(ListView):
    model = ArticlePost
    template_name = 'article/column/article_list.html'
    context_object_name = 'articles'
    paginate_by = 8


@login_required()
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


@login_required()
@csrf_exempt
def redit_article(request, article_id):
    if request.method == 'GET':
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(instance=article)
        this_article_column = article.column
        return render(request, 'article/column/redit_article.html', {
            'article': article,
            'article_columns': article_columns,
            'this_article_form': this_article_form,
            'this_article_column': this_article_column
        })
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse('1')
        except:
            return HttpResponse('2')


@login_required()
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


@login_required()
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


@login_required()
def article_detail(request, id, slug):
    context = {}
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    article.body = markdown.markdown(article.body.replace("\r\n", ' \n'), extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮拓展
        'markdown.extensions.toc'  # 自动生成目录
    ])
    context['article'] = article
    return render(request, 'article/column/article_detail.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ArticleTagView(View):
    def get(self, request):
        print('c')
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, 'article/tag/tag_list.html', {
            'article_tags': article_tags,
            'article_tag_form': article_tag_form
        })

    def post(self, request):
        print('b')
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse('1')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('数据错误')


@login_required()
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")
