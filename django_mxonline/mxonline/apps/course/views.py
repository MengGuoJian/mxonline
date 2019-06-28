# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import datetime
from django.db.models import Q

from .models import Course, CourseResource,Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequireMixin

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class CourseListView(View):

    def get(self, request):
        current_page = 'course'
        all_courses = Course.objects.order_by('-add_time')
        hot_courses = Course.objects.order_by('-click_nums')[:3]

        #  全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            #  icontains 的i的意思是不区分大小写
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))

        #  课程排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = Course.objects.order_by('-click_nums')
        elif sort == 'students':
            all_courses = Course.objects.order_by('-students')

        # orgs分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 2, request=request)
        courses = p.page(page)
        context = {
            'current_page': current_page,
            'courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,

        }
        return render(request, 'course-list.html', context=context)


class CourseDetailView(View):

    def get(self, request, course_id):
        has_fav = False
        has_fav_org = False
        course = Course.objects.get(id=int(course_id))
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_id=int(course_id), user=request.user):
                has_fav = True
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_id=course.course_org.id, fav_type=2, user=request.user):
                has_fav_org = True

        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        context = {
            'course': course,
            'has_fav': has_fav,
            'has_fav_org': has_fav_org,
            'relate_courses': relate_courses,
        }
        return render(request, 'course-detail.html', context=context)


class AddFavView(View):
    """
       用户收藏,取消收藏
    """

    def post(self, request):
        fav_type = request.POST.get('fav_type', 0)
        fav_id = request.POST.get('fav_id', 0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type="application/json")

        exit_fav = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exit_fav:
            exit_fav.delete()
            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            user_fav.user = request.user
            if int(fav_id) > 0 and int(fav_type) > 0:

                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏失败"}', content_type="application/json")


class CourseInfoView(LoginRequireMixin, View):

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #  查询用户是否已经关联起来，如果没有关联就保存创建的关联
        current_user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not current_user_course:
            current_user_course = UserCourse(user=request.user, course=course)
            course.students += 1  # 课程学习人数+1
            course.save()
            current_user_course.save()
        user_courses = UserCourse.objects.filter(course=course)  # 在用户课程里面把学过本次课程的用户课程查询出来
        user_ids = [user_course.user.id for user_course in user_courses]
        user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in user_courses]  # 把course的id都遍历出，以列表的形式保存
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:2]  #
        all_course_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'course_resources': all_course_resources,
            'relate_courses': relate_courses,
        }
        return render(request, 'course-video.html', context=context)


class CommentsView(LoginRequireMixin,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_course_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        context = {
            'course': course,
            'course_resources': all_course_resources,
            'all_comments': all_comments,
        }
        return render(request, 'course-comment.html', context=context)


class AddCommentView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"success", "msg": "用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comments = CourseComments()
            course_comments.user = request.user
            course_comments.comment = comments
            course_comments.course = course
            course_comments.save()
            return HttpResponse('{"status":"success", "msg": "评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success", "msg": "评论失败"}', content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        #  查询用户是否已经关联起来，如果没有关联就保存创建的关联
        current_user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not current_user_course:
            current_user_course = UserCourse(user=request.user, course=course)
            current_user_course.save()

        user_courses = UserCourse.objects.filter(course=course)  # 在用户课程里面把学过本次课程的用户课程查询出来
        user_ids = [user_course.user.id for user_course in user_courses]
        user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in user_courses]  # 把course的id都遍历出，以列表的形式保存
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:2]  #
        all_course_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'course_resources': all_course_resources,
            'relate_courses': relate_courses,
            'video': video,
        }
        return render(request, 'course-play.html', context=context)