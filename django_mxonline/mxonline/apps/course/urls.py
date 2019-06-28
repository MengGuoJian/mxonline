# -*- coding:utf-8 -*-
__author__ = 'meng'
__date__ = '2019/5/24 15:44'

from django.conf.urls import url

from .views import VideoPlayView,CourseListView, CourseDetailView, AddFavView, CourseInfoView, CommentsView, AddCommentView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    url(r'^video/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='video'),
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='comment'),

    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^video_play/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
]
