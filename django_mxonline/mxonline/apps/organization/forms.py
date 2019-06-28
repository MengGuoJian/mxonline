# -*- coding:utf-8 -*-
__author__ = 'meng'
__date__ = '2019/5/16 21:32'

from django import forms
import re

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['user', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']  # request请求提交的数据提取mobile
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号非法', code="mobile_invalid")
        #  否则会报出错误。