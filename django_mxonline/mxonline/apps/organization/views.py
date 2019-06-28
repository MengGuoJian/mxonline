# -*- coding=utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from course.models import Course, Teacher
from operation.models import UserFavorite

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class OrgView(View):
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        #  全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            #  icontains 的i的意思是不区分大小写
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        # 城市
        all_city = CityDict.objects.all()
        # 取出机构筛选类别
        category = request.GET.get('ct', '')
        # 热点排名：
        hot_orgs = all_orgs.order_by('-click_nums')[:3]  # 通过点击数作倒序排序，取前三个。
        if category:
            all_orgs = all_orgs.filter(catgory=category)
        # 取出筛选城市下的培训机构
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id)) # 虽然外键是city，但是在数据库里面是city_id=int(html传来的id)
        # 排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'course_nums':
            all_orgs = all_orgs.order_by('-course_nums')
        # orgs分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request, )
        orgs =p.page(page)
        # 计算有多少家机构
        orgs_nums = all_orgs.count()
        context ={
                  'all_orgs': orgs,
                  'all_city': all_city,
                  'orgs_nums': orgs_nums,
                  'city_id': city_id,
                  'category': category,
                  'hot_orgs': hot_orgs,
                  'sort': sort,
                  }
        return render(request, 'org-list.html', context=context)


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)  # commit =True可以把数据提交到数据库并且保存下来。
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            course_org.click_nums += 1
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=course_org.id)
            if user_fav:
                has_fav = True
        all_courses = course_org.course_set.all()  # 在知道course的外键的情况下，反向取出相关联的所有课程course_set
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
            })


class OrgCourseView(View):
    """
    机构课程
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()  # 在知道course的外键的情况下，反向取出相关联的所有课程course_set
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()  # 在知道course的外键的情况下，反向取出相关联的所有课程course_set
        return render(request, 'org-detail-desc.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            })


class OrgTeacherView(View):
    """
    机构教师
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            })


class AddFavView(View):
    """
    用户收藏,取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户是否登录
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        # 查询是否存在这个收藏记录，存在就删掉,取消收藏。
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            # 不存在就添加收藏
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()  # 保存到数据库
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()

        #课程讲师搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        #对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teachers":teachers,
            "sorted_teacher":sorted_teacher,
            "sort":sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_faved = True

        has_org_faved = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_org_faved = True

        #讲师排行
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request, "teacher-detail.html", {
            "teacher":teacher,
            "all_courses":all_courses,
            "sorted_teacher":sorted_teacher,
            "has_teacher_faved": has_teacher_faved,
            "has_org_faved":has_org_faved
        })