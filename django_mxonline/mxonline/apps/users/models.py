# -*- coding=utf-8 -*-
from __future__ import unicode_literals   # 第一行是python内置的
from datetime import datetime

from django.db import models             # 第二行是第三方库的
from django.contrib.auth.models import AbstractUser  # 应用自定义用户信息时候要导入的类

                                         # 第三行是自定义的库
# Create your models here.

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='')  # 昵称
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)  # 生日
    gender = models.CharField(choices=(('male', u'男'), ('female', u'女')), default=u'男', max_length=6) # 性别
    address = models.CharField(max_length=100, null=True, blank=True)  # 地址
    mobile = models.CharField(max_length=11, null=True, blank=True)  # 手机号
    image = models.ImageField(upload_to='image/%Y/%m', default=u'image/default.png', max_length=100)  # 上传图片

    class Meta:
        verbose_name = u'用户信息'         # 自定义类名
        verbose_name_plural = verbose_name

    def __unicode__(self):   # 如果不重载的话，在print profile时则不能打印我们定义的字符串
        return self.username

    def unread_nums(self):
        # 获取用户未读数量, 这里的导入是为了避免循环导入
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')  # 此处两个字段不可为空
    send_type = models.CharField(max_length=20, choices=(('register', u'注册'), ('forget', u'找回密码'),
                                                         ('update_email', u'修改邮箱')))
    send_time = models.DateTimeField(default=datetime.now)  # 注意datetime.now()后面的（）这里不需要，会报错

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图', max_length= 100) # 图片存储的路径地址
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'图片顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

