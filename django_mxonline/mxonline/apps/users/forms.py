# -*- coding:utf-8 -*-
__author__ = 'meng'
__date__ = '2019/5/5 22:45'

from django import forms

from .models import UserProfile

from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # 在做验证的时候，这个字段不能为空
    password = forms.CharField(required=True, min_length=5)  # 注意在和html里面的post的字段名一样


class RegisterForm(forms.Form):  # 不同的域会生成不同的html代码
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})  # 生成图片和验证


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})  # 生成图片和验证


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']