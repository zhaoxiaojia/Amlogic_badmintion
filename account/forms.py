from django import forms
from django.contrib.auth.models import User

from .models import UserInfo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        print('密码',password1,password2)
        if password1 != password2:
            raise forms.ValidationError(u"两次输入的密码不相同，请重新输入", code='invalid')
        return password1


class UserInfoForm(forms.ModelForm):
    # name = forms.CharField()
    # sex = forms.IntegerField()
    # depart = forms.CharField()
    # phone = forms.CharField()
    # email = forms.CharField()

    class Meta:
        model = UserInfo
        fields = ('name', 'sex', 'depart', 'phone', 'station', 'rank', 'stage','photo')
