from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


from .views import UserListView, RegisterView, myself, EditMyself
from . import views

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^detail/$', views.myself, name='detail'),
    url(r'^edit_detail/$', EditMyself.as_view(), name='edit_detail'),
    url(r'^my_image/$', views.myImage, name='my_image'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(
        template_name='account/password_change_form.html',
        success_url='/account/password_change_done/'
    ), name='password_change'),
    url(r'^password_change_done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/password_change_done.html',
    ), name='password_change_done'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset_form.html',
        email_template_name='account/password_reset_email.html',
        html_email_template_name='account/password_reset_email.html',
        success_url='/account/password_reset_done'
    ), name='password_reset'),

    url(r'^password_reset_done/$', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ), name='password_reset_done'),

    url('password_reset_confirm/(?P<uidb64>.*)/(?P<token>.*)/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html',
        success_url='/account/password_reset_complete'
    ), name='password_reset_confirm'),

    url(r'password_reset_complete/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ), name='password_reset_complete'),

]
