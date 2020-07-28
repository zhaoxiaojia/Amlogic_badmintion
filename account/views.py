from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import UserInfo
from .forms import RegisterForm, UserInfoForm
import os

ITEMS_PER_PAGE = 8


# Create your views here.


class UserListView(ListView):
    # 展示所有选手信息
    model = UserInfo
    context_object_name = 'userinfos'
    template_name = 'info_base.html'
    paginate_by = ITEMS_PER_PAGE


class RegisterView(View):
    def post(self, request):
        user_form = RegisterForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userinfo_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            userinfo = userinfo_form.save(commit=False)
            userinfo.user = new_user
            userinfo.save()
            return HttpResponseRedirect(reverse('account:login'))
        else:
            return render(request, 'account/register_fail.html',
                          {'user_form': user_form, 'userinfo_form': userinfo_form})

    def get(self, request):
        user_form = RegisterForm()
        userinfo_form = UserInfoForm()
        return render(request, 'account/register.html', {'form': user_form, 'info': userinfo_form})


@login_required()
def myself(request):
    # 展示个人信息
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,
                                                                  'userinfo') else UserInfo.objects.create(
        user=request.user)
    return render(request, 'account/detail.html', {
        'user': request.user,
        'userinfo': userinfo,
    })


@method_decorator(login_required, 'dispatch')
class EditMyself(View):
    # 修改个人信息
    def get(self, request):
        # 查询当前数据
        userinfo = UserInfo.objects.get(user_id=User.objects.get(username=request.user).id)
        # 将当前数据传至form表单
        userinfo_form = UserInfoForm(instance=userinfo)
        return render(request, 'account/edit_detail.html', {'userinfo': userinfo_form, 'info': userinfo})

    def post(self, request):
        userinfo = UserInfo.objects.get(user=request.user)
        userinfo_form = UserInfoForm(request.POST)
        if userinfo_form.is_valid():
            userinfo_cd = userinfo_form.cleaned_data
            userinfo.name = userinfo_cd['name']
            userinfo.sex = userinfo_cd['sex']
            userinfo.depart = userinfo_cd['depart']
            userinfo.phone = userinfo_cd['phone']
            userinfo.station = userinfo_cd['station']
            userinfo.rank = userinfo_cd['rank']
            userinfo.stage = userinfo_cd['stage']
            userinfo.save()
            return HttpResponseRedirect('/account/detail/')


@login_required()
def myImage(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        userinfo = UserInfo.objects.get(user_id=request.user.id)
        if userinfo.photo:
            print(userinfo.photo.url)
            if userinfo.photo.url.split('/')[-1] != photo.name:
                userinfo.photo = photo
                userinfo.save()
            else:
                print('上传的图片相同')
        else:
            userinfo.photo = photo
            userinfo.save()
        return HttpResponseRedirect('/account/detail/')
    else:
        return render(request, 'account/imagecrop.html')


def displayAnnouncement(request):
    return render(request, 'announcement.html')
