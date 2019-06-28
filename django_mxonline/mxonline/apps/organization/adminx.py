# -*- coding:utf-8 -*-
__author__ = 'meng'
__date__ = '2019/5/2 16:30'

from .models import CityDict, CourseOrg, Teacher

import xadmin


class CourseOrgAdmin(object):
    list_display = ['city', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'add_time']
    search_fields = ['city', 'name', 'desc', 'click_nums', 'fav_nums', 'image']
    list_filter = ['city', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'add_time']


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'image', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'image', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'image', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)