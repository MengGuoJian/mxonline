# -*- coding=utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from organization.models import CourseOrg, Teacher

from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=100, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath='courses/ueditor',
                          filePath='courses/ueditor', default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=10, verbose_name=u'课程难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    category = models.CharField(max_length=300, verbose_name=u'课程类别',default='')
    tag = models.CharField(default='', max_length=10, verbose_name=u'课程标签')
    needed_know = models.CharField(max_length=300, verbose_name=u'课程须知', default=u'暂时还没更新')
    teacher_tell = models.CharField(max_length=300, verbose_name=u'老师告诉你', default=u'待会儿')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lessons_nums(self):
        return self.lesson_set.all().count()
    get_lessons_nums.short_description = '章节数'

    def get_learn_users(self):
        return self.usercourse_set.all()[:3]

    def get_lessons_all(self):
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, verbose_name=u'访问地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

