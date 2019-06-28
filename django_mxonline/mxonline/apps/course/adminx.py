# -*- coding:utf-8 -*-
__author__ = 'meng'
__date__ = '2019/5/2 15:31'

from .models import Course, Lesson, Video, CourseResource

import xadmin


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  # 这样不会新建一个数据表


class CourseAdmin(object):
    list_display = ['name', 'needed_know', 'teacher_tell', 'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time', 'get_lessons_nums']
    search_fields = ['name', 'needed_know', 'teacher_tell',  'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name',  'needed_know', 'teacher_tell', 'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    inlines = [LessonInline, CourseResourceInline]
    style_fields = {"detail": "ueditor"}
    list_editable = ['degree']  # 后台编辑

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs


class BannerCourseAdmin(object):
    list_display = ['name', 'needed_know', 'teacher_tell', 'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'needed_know', 'teacher_tell',  'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name',  'needed_know', 'teacher_tell', 'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    inlines = [LessonInline, CourseResourceInline]


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name','add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name','add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name','add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)