# -*- coding:utf-8 -*-
__author__ = 'meng'
__date__ = '2019/4/28 21:45'

from .models import EmailVerifyRecord, Banner, UserProfile
from django.contrib.auth.models import User

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin


class UserProfileAdmin(UserAdmin):
    pass

class BaseSetting(object):
    enable_themes = True  # 主题
    use_bootswatch = True  # 多个主题列表


class GlobalSettings(object):
    site_title = u'慕学后台管理系统'
    site_footer = u'慕学在线网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# xadmin.site.unregister(User)  # 卸载掉User
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
#xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
