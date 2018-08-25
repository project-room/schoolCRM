import re

from decimal import Decimal
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView, TemplateView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.cache import cache
# django_pure_pagination里面的模块
from pure_pagination.mixins import PaginationMixin
from django.urls import reverse
from .forms import LoginForm, ModifyPwdForm, UploadExcelForm, UserAddForm, EditStudyInfoForm, AddBaseCourseForm, \
    AddCourseTypeForm, EditRegistrationForm

from my_signals.oplog_signal import op_log
from .forms import LoginForm, ModifyPwdForm, UploadExcelForm, UserAddForm
from .models import *
from schoolCRM.settings import SESSION_COOKIE_AGE
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.hashers import make_password
from course.models import CourseType, Course, ParentCourse
import json
import time
import xlrd
import xlwt
import datetime

from utils.excel_tool import create_courseinfo_excel, create_registerinfo_excel, create_registerinfo_excel_table, \
    create_studyinfo_excel_table
import operator
from functools import reduce


# Create your views here.

class LoginIndexView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        redirect_url = request.GET.get('next', 'course')
        return render(request, "login.html", {
            "redirect_url": redirect_url
        })

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # 下次自动登录
                    auto_login = request.POST.getlist("auto_login")
                    if auto_login:
                        request.session.set_expiry(SESSION_COOKIE_AGE)

                    op_log.send(
                        sender=Oplog,
                        admin=request.user,
                        reason=user_name+"登入系统"
                    )
                    return JsonResponse({"status": "success"}, safe=False)
            else:
                cache.get_or_set(user_name, 0, timeout=24 * 60 * 60)
                new_error_num = cache.incr(user_name)
                error_msg = "用户名或密码错误!"
                if new_error_num > 3:
                    error_msg = "该用户密码输入超过3次，请联系管理员！"
                return_data = {
                    "status": "failed",
                    "error_msg": error_msg,
                    "return_username": user_name,
                    "return_password": pass_word,
                }
                return JsonResponse(return_data, safe=False)
        else:
            return render(
                request, "login.html", {
                    "login_form": login_form})


class LogOutView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        op_log.send(
            sender=Oplog,
            admin=request.user,
            reason=str(request.user.username)+"登出系统"
        )
        logout(request)
        return HttpResponseRedirect(reverse("log_in"))


# 上课信息列表
class StudyListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    queryset = CourseInfo.objects.filter(is_deleted=0)
    template_name = 'lesson/lesson.html'
    paginate_by = 8
    context_object_name = "courseinfos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_types"] = CourseType.objects.all()
        context["courses"] = Course.objects.all()
        context["parent_courses"] = ParentCourse.objects.all()
        context["teachers"] = Teacher.objects.filter(is_deleted=0)
        context["students"] = Student.objects.filter(is_deleted=0)
        return context


class AddStudyInfoAjaxView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        student_id_str_list = json.loads(request.POST.get("student_id_list"))
        student_id_list = set([int(student_id) for student_id in student_id_str_list])
        study_date = request.POST.get("study_date", "")
        study_hours = request.POST.get("study_hours", "")
        study_course_id = request.POST.get("study_course_id", "")
        study_employee_id = request.POST.get("study_employee_id", "")
        study_course_type_id = request.POST.get("study_course_type_id", "")
        for student_id in student_id_list:
            # 添加上课日志
            student=Student.objects.filter(id=student_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="添加" + student.name + "上课信息"
            )


            register_totals = register_info = RegisterInfo.objects.filter(student_id=student_id, is_deleted=0)
            register_total_time = 0
            for register_total in register_totals:
                register_total_time += register_total.hours

            course_totals = CourseInfo.objects.filter(student_id=student_id, is_deleted=0)
            course_total_time = 0
            for course_total in course_totals:
                course_total_time += course_total.remaining_time

            course_info = CourseInfo(remaining_time=register_total_time - course_total_time - int(study_hours),
                                     hours=study_hours, class_date=study_date, is_deleted=0,
                                     course_id=int(study_course_id),
                                     teacher_id=int(study_employee_id), course_type_id=int(study_course_type_id),
                                     student_id=student_id)
            course_info.save()


        return JsonResponse({"status": "success"}, safe=False)


class StudyInfoView(LoginRequiredMixin, DetailView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        studyinfo_id = request.POST.get("studyinfo_id", "")
        studyinfo = CourseInfo.objects.get(pk=int(studyinfo_id))
        context = {
            "status": "success",
            "studyinfo_id": studyinfo.id,
            "course": studyinfo.course.course_name,
            "class_data": studyinfo.class_date,
            "student_name": studyinfo.student.name,
            "stu_FN": studyinfo.student.first_name,
            "stu_LN": studyinfo.student.last_name,
            "hours": studyinfo.course.hours,
            "emp_num": studyinfo.teacher.employee_num,
            "teacher_name": studyinfo.teacher.name
        }
        return JsonResponse(context, safe=False)


# 上课信息页面详情
class StudyInfoDetailView(LoginRequiredMixin, DetailView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    model = CourseInfo
    template_name = "lesson/studyinfo_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["study_info"] = CourseInfo.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg), is_deleted=0).first()
        context["courses"] = Course.objects.all()
        context["students"] = Student.objects.filter(is_deleted=0)
        context["teachers"] = Teacher.objects.filter(is_deleted=0)
        context["course_types"] = CourseType.objects.all()
        context["param_study"] = self.request.get_full_path()
        return context


# 上课信息编辑完后进行保存
class StudyInfoEditSaveView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        study_form = EditStudyInfoForm(request.POST)
        if study_form.is_valid():
            studyinfo_id_hidden = request.POST.get("studyinfo_id_hidden", "")
            studyinfo_course = request.POST.get("studyinfo_course", "")
            studyinfo_course_type = request.POST.get("course_type_name", "")
            studyinfo_hours = request.POST.get("studyinfo_hours", "")
            studyinfo_class_date = request.POST.get("studyinfo_class_date", "")
            study_student_id = request.POST.get("study_student_id", "")
            study_teacher_id = request.POST.get("study_teacher_id", "")
            course_info = CourseInfo.objects.filter(pk=int(studyinfo_id_hidden)).first()
            course_info.course = Course.objects.filter(pk=int(studyinfo_course)).first()
            course_info.course_type = CourseType.objects.filter(pk=int(studyinfo_course_type)).first()
            course_info.hours = studyinfo_hours
            course_info.class_date = studyinfo_class_date
            course_info.student = Student.objects.filter(pk=int(study_student_id)).first()
            course_info.teacher = Teacher.objects.filter(pk=int(study_teacher_id)).first()
            course_info.save()
            return JsonResponse({"status": "success"}, safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)


# 上课信息查询
class StudyInfoSearchView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = 'lesson/lesson.html'
    paginate_by = 8
    context_object_name = "courseinfos"

    def get_queryset(self):

        name = self.request.GET.get('name', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        course_id = self.request.GET.get("course_id", None)
        course_type_id = self.request.GET.get('course_type_id', None)

        data_list = CourseInfo.objects.filter(is_deleted=0)
        if name:
            data_list = data_list.filter(Q(student__name__icontains=name) | Q(teacher__name__icontains=name))
        if course_type_id:
            data_list = data_list.filter(course_type=CourseType.objects.filter(pk=int(course_type_id)).first())
        if course_id:
            data_list = data_list.filter(course=Course.objects.filter(pk=int(course_id)).first())
        if start_date and end_date:
            data_list = data_list.filter(class_date__range=(start_date, end_date))
        if start_date and (not end_date):
            data_list = data_list.filter(class_date__gte=start_date)
        if (not start_date) and end_date:
            data_list = data_list.filter(class_date__lte=end_date)
        return data_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()
        context["course_types"] = CourseType.objects.filter()
        context["parent_courses"] = ParentCourse.objects.all()
        context["param_study_search"] = self.request.path
        return context


class DeleteStudyInfoByIdView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        courseinfo_id = request.POST.get("courseinfo_id", "")
        CourseInfo.objects.filter(pk=courseinfo_id).update(is_deleted=1, delete_date=datetime.date.today())
        context = {
            "status": "success"
        }
        return JsonResponse(context, safe=False)


class DeleteStudyInfoView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy")
        for course_info_id in checkbox_list:
            # 删除上课日志
            courseInfo=CourseInfo.objects.filter(id=course_info_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="删除" + courseInfo.student.name + "上课信息"
            )

            CourseInfo.objects.filter(id=course_info_id).update(is_deleted=1, delete_date=datetime.date.today())


        return HttpResponseRedirect(reverse("lesson"))


# 人员管理
class SettingsView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    queryset = UserProfile.objects.filter(is_deleted=0)
    template_name = 'settings/setting.html'
    paginate_by = 8


class AccountView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        # TODO 在所有视图加上is_active判断
        user = UserProfile.objects.get(pk=request.user.id)
        return render(request, "account.html", {"user": user})


class SettingsEditView(LoginRequiredMixin, DetailView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    model = UserProfile
    template_name = "settings/setting_edit.html"
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = UserProfile.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg),
                                                             is_deleted=0).first()
        context["param_set"] = self.request.get_full_path()
        return context


class TopSettingsEditView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        data_id = int(request.GET.get("data_id", ""))
        user_profile = UserProfile.objects.get(pk=data_id)
        context = {
            "user_profile": user_profile
        }
        return render(request, "settings/setting_edit.html", context=context)


# 人员条件查询
class SettingsUserSearchView(LoginRequiredMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = 'settings/setting.html'
    paginate_by = 8

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        data_list = UserProfile.objects.filter(is_deleted=0)
        if name:
            data_list = data_list.filter(Q(username=name) | Q(real_name=name))
        return data_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["param_set_search"] = self.request.path
        return context


class SettingsUserForbidView(LoginRequiredMixin, View):
    """
    用户勾选了某一条用户记录，再点击禁用按钮，
    alert("是否要禁用")，用户点击了确定之后，
    页面刷新，
    第三列显示红色的禁用图标
    """

    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            UserProfile.objects.filter(id__in=checkbox_list).update(is_active=False)

        # 禁用用户日志
        for user_id in checkbox_list:
            user=UserProfile.objects.filter(id=user_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="禁用" + user.real_name + "用户"
            )
        return HttpResponseRedirect(reverse("settings"))


class SettingsUserAddView(LoginRequiredMixin, TemplateView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    template_name = "settings/setting_add.html"


class SettingsUserAddSaveView(LoginRequiredMixin, View):
    """
    人员管理这个tab添加人员
    流程：
    输入内容后，点击添加
    ajax提交表单，UserProfile表生成数据，
    返回请稍后
    成功之后，返回添加成功
    返回人员管理首页
    """
    template_name = "settings/setting_add.html"

    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        user_add_form = UserAddForm(request.POST)
        if user_add_form.is_valid():
            username = request.POST.get("username", "")
            username_is_exist = UserProfile.objects.filter(username=username).first()
            if username_is_exist:
                return JsonResponse(user_add_form.errors)
            else:
                pwd = request.POST.get("pwd", "")
                ack_pwd = request.POST.get("ack_pwd", "")
                real_name = request.POST.get("real_name", "")
                # must_change_pwd = request.POST.get("must_change_pwd", "")
                if pwd != ack_pwd:
                    return JsonResponse(
                        {"status": "fail", "msg": "密码不一致"}, safe=False
                    )
                UserProfile.objects.create(username=username,
                                           password=make_password(ack_pwd),
                                           real_name=real_name)
                op_log.send(
                    sender=Oplog,
                    admin=request.user,
                    reason="添加" + real_name + "用户"
                )

                return JsonResponse(
                    {"status": "success"}, safe=False
                )
        else:
            return JsonResponse(user_add_form.errors)


# 编辑人员
class SettingsUserEditSaveView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        edit_form = UserAddForm(request.POST)
        if edit_form.is_valid():
            hiddle_user_id = request.POST.get("hiddle_user_id", "")
            username = request.POST.get("username", "")
            pwd = request.POST.get("pwd", "")
            ack_pwd = request.POST.get("ack_pwd", "")
            real_name = request.POST.get("real_name", "")
            # must_change_pwd = request.POST.get("must_change_pwd", "")
            active_status = request.POST.get("active_status", "")
            if pwd != ack_pwd:
                return JsonResponse(
                    {"status": "fail", "msg": "密码不一致"}, safe=False
                )

            if active_status == "1":
                UserProfile.objects.filter(pk=int(hiddle_user_id)).update(username=username,
                                                                          password=make_password(ack_pwd),
                                                                          real_name=real_name,
                                                                          is_active=True)
            else:
                UserProfile.objects.filter(pk=int(hiddle_user_id)).update(username=username,
                                                                          password=make_password(ack_pwd),
                                                                          real_name=real_name)

            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="修改" + username + "用户"
            )
            return JsonResponse({"status": "success"}, safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)


# 删除人员
class SettingsUserDeleteView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request, user_id):
        UserProfile.objects.filter(pk=user_id).update(is_deleted=1)
        return HttpResponseRedirect(reverse("settings"))

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            UserProfile.objects.filter(id__in=checkbox_list).update(is_deleted=1)
        return HttpResponseRedirect(reverse("settings"))


# 账号设置
class ModifyPwdView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            ori_pwd = request.POST.get("ori_pwd", "")
            new_pwd = request.POST.get("new_pwd", "")
            ack_pwd = request.POST.get("ack_pwd", "")
            # 如果两次密码不相等，返回错误信息
            if new_pwd != ack_pwd:
                return JsonResponse(
                    {"status": "fail", "msg": "密码不一致"}, safe=False
                )
            ack_user = authenticate(username=request.user.username, password=ori_pwd)

            if ack_user is not None:
                ack_user.password = make_password(ack_pwd)
                # save保存到数据库
                ack_user.save()
                op_log.send(
                    sender=Oplog,
                    admin=request.user,
                    reason=request.user.username+"修改密码"
                )
                return JsonResponse(
                    {"status": "success"}, safe=False
                )
            else:
                return JsonResponse(
                    {"status": "failed"}, safe=False
                )
        # 验证失败说明密码位数不够。
        else:
            # 通过json的dumps方法把字典转换为json字符串
            return JsonResponse(modify_form.errors)

# 导出上课信息
class StudyInfoExcelCreateView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        excel_str_id_list = json.loads(self.request.POST.get("excel_id_list"))
        excel_id_list = [int(i) for i in excel_str_id_list]
        request.session["excel_id_list"] = excel_id_list
        return JsonResponse({"status": "success"}, safe=False)

# 导出上课信息
class StudyInfoExcelEmitView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        excel_id_list = request.session.get("excel_id_list", "")
        if "excel_id_list" in request.session.keys():
            del request.session['excel_id_list']
        if excel_id_list:
            emit_info = CourseInfo.objects.filter(id__in=excel_id_list, is_deleted=0)
        else:
            emit_info = CourseInfo.objects.filter(is_deleted=0)
        f = create_courseinfo_excel(emit_info)

        # 导出上课信息日志
        for courseInfo in emit_info:
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="导出" + courseInfo.student.name + "上课信息"
            )

        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % current_time
        f.save(response)
        return response


# 导入上课信息
class StudyInfoExcelImportView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        excel_form = UploadExcelForm(request.POST, request.FILES)
        if excel_form.is_valid():
            wb = xlrd.open_workbook(
                filename=None, file_contents=request.FILES['excel'].read())  # 关键点在于这里
        else:
            msg = "请选择要导入的Excel表"
            return JsonResponse({
                'status': 'error',
                'msg': msg
            })
        table = wb.sheets()[0]
        table_num = table.nrows
        course_info_list = []
        for i in range(1, table_num):
            data = table.row_values(i)
            try:
                if not data[0] or not data[1] or not data[2] or not data[3] or not data[4] or not data[5] or data[
                    6] == "" or not data[7] or not data[8] or not data[9]:
                    msg = "第" + str(i + 1) + "行数据不能为空！，导入失败！"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })

                course_result = Course.objects.filter(course_name=data[0],
                                                      parent_name=ParentCourse.objects.filter(
                                                          name__icontains=re.match(r"\D+", data[0]).group()).first())
                if course_result.count() < 1:
                    msg = "第" + str(i + 1) + "行" + data[0] + "课程不存在，导入失败!"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })

                teacher_result = Teacher.objects.filter(name=data[9], employee_num=str(self._to_int(data[8])))
                if teacher_result.count() < 1:
                    msg = "第" + str(i + 1) + "行" + data[9] + "教师不存在，导入失败!"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })

                course_type_result = CourseType.objects.filter(type_name=data[7])
                if course_type_result.count() < 1:
                    msg = "第" + str(i + 1) + "行" + data[7] + "课程类型不存在，导入失败!"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })

                student_result = Student.objects.filter(name=data[2], first_name=data[4], last_name=data[3],
                                                        phone=str(self._to_int(data[5])))
                if student_result.count() < 1:
                    student = Student(name=data[2], first_name=data[4], last_name=data[3],
                                      phone=str(self._to_int(data[5])))
                    student.save()

                single_course_info = CourseInfo.objects.filter(
                    hours=str(self._to_int(data[6])),
                    course=Course.objects.filter(course_name=data[0],
                                                 parent_name=ParentCourse.objects.filter(
                                                     name__icontains=re.match(r"\D+",
                                                                              data[0]).group()).first()).first(),
                    student=Student.objects.filter(name=data[2], first_name=data[4], last_name=data[3],
                                                   phone=str(self._to_int(data[5]))).first(),
                    teacher=Teacher.objects.filter(name=data[9], employee_num=str(self._to_int(data[8]))).first(),
                    class_date=xlrd.xldate.xldate_as_datetime(data[1], 0),
                    course_type=CourseType.objects.filter(type_name=data[7]).first())
                if single_course_info.count() >= 1:
                    msg = "第" + str(i + 1) + "行上课信息已存在！，导入失败！"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })

                else:
                    single_course_info = CourseInfo(
                        hours=str(self._to_int(data[6])),
                        course=Course.objects.filter(course_name=data[0],
                                                     parent_name=ParentCourse.objects.filter(
                                                         name__icontains=re.match(r"\D+",
                                                                                  data[0]).group()).first()).first(),
                        student=Student.objects.filter(name=data[2], first_name=data[4], last_name=data[3],
                                                       phone=str(self._to_int(data[5]))).first(),
                        teacher=Teacher.objects.filter(name=data[9], employee_num=str(self._to_int(data[8]))).first(),
                        class_date=xlrd.xldate.xldate_as_datetime(data[1], 0),
                        course_type=CourseType.objects.filter(type_name=data[7]).first()
                    )
                    course_info_list.append(single_course_info)
            except:
                msg = "导入失败，请核查导入的表是否正确！"
                return JsonResponse({
                    'status': 'error',
                    'msg': msg
                })

        CourseInfo.objects.bulk_create(course_info_list)

        for course_info in course_info_list:
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="导入"+course_info.student.name+"上课信息"
            )
        msg = "导入成功！"
        return JsonResponse({
            'status': 'ok',
            'msg': msg
        })

    @staticmethod
    def _to_int(text):
        try:
            i = int(text)
        except ValueError:
            return text

        if i == text:
            return i
        else:
            return text


# 回收站
class RegisterTrashListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = 'recycle/recycle_register.html'
    paginate_by = 8

    def get_queryset(self):
        return RegisterInfo.objects.filter(is_deleted=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["param_register_recyle"] = self.request.path
        return context


class StudyInfoTrashListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = 'recycle/recycle.html'
    paginate_by = 8

    def get_queryset(self):
        return CourseInfo.objects.filter(is_deleted=1)


class StudentTrashListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = 'recycle/recycle_student.html'
    paginate_by = 8

    def get_queryset(self):
        return Student.objects.filter(is_deleted=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["param_stu_recyle"] = self.request.path
        return context


class TeacherTrashListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = 'recycle/recycle_teacher.html'
    paginate_by = 8

    def get_queryset(self):
        return Teacher.objects.filter(is_deleted=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["param_teach_recyle"] = self.request.path
        return context


class PeopleTrashListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = 'recycle/recycle_people.html'
    paginate_by = 8

    def get_queryset(self):
        return UserProfile.objects.filter(is_deleted=1)

# 回收站上课信息还原
class StudyInfoTrashRedoView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = int(request.GET.get("course_info_id", ""))
        CourseInfo.objects.filter(pk=pk).update(is_deleted=0)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            CourseInfo.objects.filter(id__in=checkbox_list).update(is_deleted=0)

        # 回收站还原信息日志
        for course_id in checkbox_list:
            course=CourseInfo.objects.filter(id=course_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="还原" + course.student.name + "上课信息"
            )
        return HttpResponseRedirect(reverse("recycle"))

# 回收站删除上课信息
class StudyInfoTrashDeleteForeverView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = request.GET.get("course_info_id", "")
        CourseInfo.objects.filter(pk=pk).update(is_deleted=2)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            CourseInfo.objects.filter(id__in=checkbox_list).update(is_deleted=2)

        for course_id in checkbox_list:
            courseInfo=CourseInfo.objects.filter(id=course_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="删除回收站"+courseInfo.student.name+"上课信息"
            )

        return HttpResponseRedirect(reverse("recycle"))


# 删除回收站教师信息
class TeacherInfoTrashDeleteForeverView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = request.GET.get("teacher_info_id", "")
        Teacher.objects.filter(pk=pk).update(is_deleted=2)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            Teacher.objects.filter(id__in=checkbox_list).update(is_deleted=2)

        for teacher_id in checkbox_list:
            teacher=Teacher.objects.filter(id=teacher_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="删除回收站" + teacher.name + "教师信息"
            )
        return HttpResponseRedirect(reverse("recycle_teacher"))


# 删除回收站报名信息
class RegisterInfoTrashDeleteForeverView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = request.GET.get("register_info_id", "")
        RegisterInfo.objects.filter(pk=pk).update(is_deleted=2)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            RegisterInfo.objects.filter(id__in=checkbox_list).update(is_deleted=2)

        for register_id in checkbox_list:
            register= RegisterInfo.objects.filter(id=register_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="删除回收站" + register.student.name + "报名信息"
            )
        return HttpResponseRedirect(reverse("recycle_register"))


# 回收站删除学生信息
class StudentTrashDeleteForeverView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = int(request.GET.get("student_info_id", ""))
        Student.objects.filter(pk=pk).update(is_deleted=2)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            Student.objects.filter(id__in=checkbox_list).update(is_deleted=2)

        for student_id in checkbox_list:
            student=Student.objects.filter(id=student_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="删除回收站" + student.name + "学生信息"
            )
        return HttpResponseRedirect(reverse("recycle_stu"))


# 回收站删除人员信息
class PeopleTrashDeleteForeverView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = int(request.GET.get("people_info_id", ""))
        UserProfile.objects.filter(pk=pk).update(is_deleted=2)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            UserProfile.objects.filter(id__in=checkbox_list).update(is_deleted=2)
        return HttpResponseRedirect(reverse("recycle_people"))

# 回收站教师信息还原
class TeacherTrashRedoView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = int(request.GET.get("teacher_info_id", ""))
        Teacher.objects.filter(pk=pk).update(is_deleted=0)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            Teacher.objects.filter(id__in=checkbox_list).update(is_deleted=0)

        for teacher_id in checkbox_list:
            teacher=Teacher.objects.filter(id=teacher_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="还原" + teacher.name + "教师信息"
            )
        return HttpResponseRedirect(reverse("recycle_teacher"))


# 回收站报名信息还原
class RegisterTrashRedoView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = int(request.GET.get("register_info_id", ""))
        RegisterInfo.objects.filter(pk=pk).update(is_deleted=0)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            RegisterInfo.objects.filter(id__in=checkbox_list).update(is_deleted=0)

        for register_id in checkbox_list:
            register=RegisterInfo.objects.filter(id=register_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="还原" + register.student.name + "报名信息"
            )
        return HttpResponseRedirect(reverse("recycle_register"))

# 回收站还原学生信息
class StudentTrashRedoView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            Student.objects.filter(id__in=checkbox_list).update(is_deleted=0)

        for student_id in checkbox_list:
            student=Student.objects.filter(id=student_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="还原" + student.name + "学生信息"
            )
        return HttpResponseRedirect(reverse("recycle_stu"))

    def get(self, request):
        pk = int(request.GET.get("student_info_id", ""))
        Student.objects.filter(pk=pk).update(is_deleted=0)
        return JsonResponse({"status": "success"}, safe=False)


class PeopleTrashRedoView(LoginRequiredMixin, PaginationMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        pk = int(request.GET.get("people_info_id", ""))
        UserProfile.objects.filter(pk=pk).update(is_deleted=0)
        return JsonResponse({"status": "success"}, safe=False)

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            UserProfile.objects.filter(id__in=checkbox_list).update(is_deleted=0)
        return HttpResponseRedirect(reverse("recycle_people"))


# 报名信息列表
class RegistrationView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    queryset = RegisterInfo.objects.filter(is_deleted=0)
    template_name = 'registration/registration.html'
    paginate_by = 8
    context_object_name = "registioninfos"

    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_courses"] = ParentCourse.objects.all()
        context["course_types"] = CourseType.objects.all()
        context["courses"] = Course.objects.all()
        context["students"] = Student.objects.filter(is_deleted=0)

        return context


# 报名信息条件查询
class RegistrationSearchView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = "/log_in/"
    redirect_field_name = "next"
    paginate_by = 8
    context_object_name = "registioninfos"
    template_name = "registration/registration.html"

    def get_queryset(self):
        stu_name = self.request.GET.get('stu_name', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        course_id = self.request.GET.get("course_id", None)
        course_type_id = self.request.GET.get("course_type_id", None)
        data_list = RegisterInfo.objects.filter(is_deleted=0)
        if stu_name:
            data_list = data_list.filter(Q(student__name__icontains=stu_name))
        if course_id:
            data_list = data_list.filter(course=Course.objects.filter(pk=int(course_id)).first())
        if course_type_id:
            data_list = data_list.filter(course_type=CourseType.objects.filter(pk=int(course_type_id)).first())
        if start_date and end_date:
            data_list = data_list.filter(register_date__range=(start_date, end_date))
        if start_date and (not end_date):
            data_list = data_list.filter(register_date__gte=start_date)
        if (not start_date) and end_date:
            data_list = data_list.filter(register_date__lte=end_date)
        return data_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_courses"] = ParentCourse.objects.all()
        context["course_types"] = CourseType.objects.all()
        context["param_register_search"] = self.request.path

        return context

    """
    删除报名信息
    """


class RegistrationDeleteView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy", "")
        if checkbox_list:
            RegisterInfo.objects.filter(id__in=checkbox_list).update(is_deleted=1, delete_date=datetime.date.today())

        # 删除报名日志
        for register_id in checkbox_list:
            register=RegisterInfo.objects.filter(id=register_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="删除" + register.student.name + "报名信息"
            )
        return HttpResponseRedirect(reverse("registration"))


class BaseSettingsView(TemplateView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    template_name = 'basesetting/baseSetting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_types"] = CourseType.objects.all()
        context["parent_courses"] = ParentCourse.objects.all()
        return context


class BaseSettingsAjaxView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        context = {}
        context["course_types"] = CourseType.objects.all()
        context["parent_courses"] = ParentCourse.objects.all()
        context["children_courses"] = Course.objects.all()
        course_types = []

        return JsonResponse(context, safe=False)


# 删除基本信息
class BaseSettingsDelete(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        parent_course_detail_list = request.POST.getlist("parent_course_detail", "")
        children_course_detail_list = request.POST.getlist("children_course_detail", "")
        course_type_detail_list = request.POST.getlist("course_type_detail", "")
        parent_id_list = [int(parent_id) for parent_id in parent_course_detail_list]
        children_id_list = [int(children_id) for children_id in children_course_detail_list]
        type_id_list = [int(type_id) for type_id in course_type_detail_list]
        if type_id_list:
            # 删除日志
            for type_id in type_id_list:
                course_type=CourseType.objects.filter(id=type_id).first()
                op_log.send(
                    sender=Oplog,
                    admin=request.user,
                    reason="删除"+course_type.type_name+"类型"
                )

            CourseType.objects.filter(id__in=type_id_list).delete()
        elif parent_id_list:
            # 删除日志
            for children_id in children_id_list:
                course=Course.objects.filter(id=children_id).first()
                op_log.send(
                    sender=Oplog,
                    admin=request.user,
                    reason="删除" + course.course_name + "子课程"
                )

            Course.objects.filter(id__in=children_id_list).delete()

            # 删除日志
            for parent_id in parent_id_list:
                parentCourse=ParentCourse.objects.filter(id=parent_id).first()
                op_log.send(
                    sender=Oplog,
                    admin=request.user,
                    reason="删除" + parentCourse.name + "父课程"
                )

            ParentCourse.objects.filter(id__in=parent_id_list).delete()
        else:
            for children_id in children_id_list:
                course=Course.objects.filter(id=children_id).first()
                op_log.send(
                    sender=Oplog,
                    admin=request.user,
                    reason="删除" + course.course_name + "子课程"
                )

            Course.objects.filter(id__in=children_id_list).delete()

        return HttpResponseRedirect(reverse("basesettings"))


# 基础课程详情
class BaseSettingsDetail(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        parent_course_id = request.POST.get("parent_course_id", "")
        parent_course = ParentCourse.objects.filter(pk=int(parent_course_id)).first()
        courses = Course.objects.filter(parent_name=parent_course)

        children_list = []
        for course in courses:
            children = {}
            children["children_id"] = course.id
            children["children_course_name"] = course.course_name
            children_list.append(children)
        context = {
            "status": "success",
            "parent_id": parent_course.id,
            "parent_name": parent_course.name,
            "children_list": children_list
        }
        return JsonResponse(context, safe=False)


# 基础课程类型详情
class BaseTypesDetail(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        course_type_id = request.POST.get("course_type_id", "")
        course_type = CourseType.objects.filter(pk=int(course_type_id)).first()
        context = {
            "status": "success",
            "course_type_id": course_type.id,
            "course_type_name": course_type.type_name,
        }
        return JsonResponse(context, safe=False)


# 获取父课程ajax
class GetParentCoursesView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        parent_courses = ParentCourse.objects.all()
        parent_course_list = []
        for parent_course in parent_courses:
            parent = {}
            parent["parent_course_id"] = parent_course.id
            parent["parent_course_name"] = parent_course.name
            parent_course_list.append(parent)
        context = {
            "status": "success",
            "parent_courses": parent_course_list
        }
        return JsonResponse(context, safe=False)


# 添加课程
class AddBaseCourseView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        course_form = AddBaseCourseForm(request.POST)
        if course_form.is_valid():
            parent_course_name = request.POST.get("parent_course_name", "")
            children_course_name = request.POST.get("children_course_name", "")
            parent = ParentCourse.objects.filter(name=parent_course_name).first()
            if parent:
                if children_course_name:
                    children_course = Course.objects.filter(course_name=children_course_name).first()
                    if children_course:
                        return JsonResponse({"status": "fail"}, safe=False)
                    else:
                        course = Course(course_name=children_course_name)
                        course.parent_name = parent
                        course.save()
                        op_log.send(
                            sender=Oplog,
                            admin=request.user,
                            reason="添加" + children_course_name + "子课程"
                        )
                        return JsonResponse({"status": "success"}, safe=False)
                else:
                    return JsonResponse({"status": "fail"}, safe=False)
            else:
                ParentCourse.objects.create(name=parent_course_name)
                if children_course_name:
                    course = Course(course_name=children_course_name)
                    course.parent_name = ParentCourse.objects.filter(name=parent_course_name).first()
                    course.save()
                    op_log.send(
                        sender=Oplog,
                        admin=request.user,
                        reason="添加父课程" +parent_course_name+"子课程"+children_course_name
                    )
                    return JsonResponse({"status": "success"}, safe=False)
                else:
                    op_log.send(
                        sender=Oplog,
                        admin=request.user,
                        reason="添加" + parent_course_name + "父课程"
                    )
                    return JsonResponse({"status": "success"}, safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)


# 添加课程类型
class AddCourseTypeView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        course_type_form = AddCourseTypeForm(request.POST)
        if course_type_form.is_valid():
            add_course_type = request.POST.get("add_course_type", "")
            course_type = CourseType.objects.filter(type_name=add_course_type).first()
            if course_type:
                return JsonResponse({"status": "fail"}, safe=False)
            else:
                CourseType.objects.create(type_name=add_course_type)
                op_log.send(
                    sender=Oplog,
                    admin=request.user,
                    reason="添加" + add_course_type + "类型"
                )
                return JsonResponse({"status": "success"}, safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)


# 修改父课程名
class UpdateParentCourseNameView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        parent_course_id = request.POST.get("parent_course_id", "")
        parent_course_name = request.POST.get("parent_course_name", "")
        ParentCourse.objects.filter(pk=int(parent_course_id)).update(name=parent_course_name)

        course_types = CourseType.objects.all()
        parent_courses = ParentCourse.objects.all()

        course_type_list = []
        parent_course_list = []
        # children_course_list = []

        for course_type in course_types:
            course_type_info = {}
            course_type_info["course_type_id"] = course_type.id
            course_type_info["course_type_name"] = course_type.type_name
            course_type_list.append(course_type_info)

        for parent_course in parent_courses:
            children_courses = parent_course.course_set.get_queryset()
            children_course_list = []
            for children_course in children_courses:
                children_course_info = {}
                children_course_info["children_course_id"] = children_course.id
                children_course_info["children_course_name"] = children_course.course_name
                children_course_list.append(children_course_info)

            parent_course_info = {}
            parent_course_info["parent_course_id"] = parent_course.id
            parent_course_info["parent_course_name"] = parent_course.name
            parent_course_info["parent_childrens"] = children_course_list
            parent_course_list.append(parent_course_info)

        context = {
            "status": "success",
            "course_types": course_type_list,
            "parent_courses": parent_course_list,
        }

        op_log.send(
            sender=Oplog,
            admin=request.user,
            reason="修改" + parent_course_name + "父课程"
        )

        return JsonResponse(context, safe=False)


# 修改子课程名
class UpdateChildrenCourseNameView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        child_course_id = request.POST.get("child_course_id", "")
        child_course_name = request.POST.get("child_course_name", "")
        Course.objects.filter(pk=int(child_course_id)).update(course_name=child_course_name)

        course_types = CourseType.objects.all()
        parent_courses = ParentCourse.objects.all()

        course_type_list = []
        parent_course_list = []

        for course_type in course_types:
            course_type_info = {}
            course_type_info["course_type_id"] = course_type.id
            course_type_info["course_type_name"] = course_type.type_name
            course_type_list.append(course_type_info)

        for parent_course in parent_courses:
            children_courses = parent_course.course_set.get_queryset()
            children_course_list = []
            for children_course in children_courses:
                children_course_info = {}
                children_course_info["children_course_id"] = children_course.id
                children_course_info["children_course_name"] = children_course.course_name
                children_course_list.append(children_course_info)

            parent_course_info = {}
            parent_course_info["parent_course_id"] = parent_course.id
            parent_course_info["parent_course_name"] = parent_course.name
            parent_course_info["parent_childrens"] = children_course_list
            parent_course_list.append(parent_course_info)

        context = {
            "status": "success",
            "course_types": course_type_list,
            "parent_courses": parent_course_list,
        }
        op_log.send(
            sender=Oplog,
            admin=request.user,
            reason="修改" + child_course_name + "子课程"
        )
        return JsonResponse(context, safe=False)


# 修课程类型名
class UpdateCourseTypeNameView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        course_type_id = request.POST.get("course_type_id", "")
        course_type_name = request.POST.get("course_type_name", "")
        CourseType.objects.filter(pk=int(course_type_id)).update(type_name=course_type_name)

        course_types = CourseType.objects.all()
        parent_courses = ParentCourse.objects.all()

        course_type_list = []
        parent_course_list = []

        for course_type in course_types:
            course_type_info = {}
            course_type_info["course_type_id"] = course_type.id
            course_type_info["course_type_name"] = course_type.type_name
            course_type_list.append(course_type_info)

        for parent_course in parent_courses:
            children_courses = parent_course.course_set.get_queryset()
            children_course_list = []
            for children_course in children_courses:
                children_course_info = {}
                children_course_info["children_course_id"] = children_course.id
                children_course_info["children_course_name"] = children_course.course_name
                children_course_list.append(children_course_info)

            parent_course_info = {}
            parent_course_info["parent_course_id"] = parent_course.id
            parent_course_info["parent_course_name"] = parent_course.name
            parent_course_info["parent_childrens"] = children_course_list
            parent_course_list.append(parent_course_info)

        context = {
            "status": "success",
            "course_types": course_type_list,
            "parent_courses": parent_course_list,
        }

        op_log.send(
            sender=Oplog,
            admin=request.user,
            reason="修改" + course_type_name + "类型"
        )

        return JsonResponse(context, safe=False)


# 获取总课程
class GetBaseSettingCourseView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        parent_courses = ParentCourse.objects.all()
        parent_course_list = []
        for parent_course in parent_courses:
            parent_course_info = {}
            parent_course_info["parent_course_id"] = parent_course.id
            parent_course_info["parent_course_name"] = parent_course.name

            children_courses = parent_course.course_set.get_queryset()
            children_course_list = []
            for children_course in children_courses:
                children_course_info = {}
                children_course_info["children_course_id"] = children_course.id
                children_course_info["children_course_name"] = children_course.course_name
                children_course_list.append(children_course_info)
            parent_course_info["parent_childrens"] = children_course_list
            parent_course_list.append(parent_course_info)

        context = {
            "status": "success",
            "parent_course_total": parent_course_list
        }
        return JsonResponse(context, safe=False)


# 获取总课程类型
class GetBaseSettingTypeView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        course_types = CourseType.objects.all()
        course_type_list = []
        for course_type in course_types:
            course_type_info = {}
            course_type_info["course_type_id"] = course_type.id
            course_type_info["course_type_name"] = course_type.type_name
            course_type_list.append(course_type_info)
        context = {
            "status": "success",
            "course_type_total": course_type_list
        }
        return JsonResponse(context, safe=False)


# 报名信息的添加
class AddRegistrationView(LoginRequiredMixin, TemplateView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    template_name = "registration/registrationAdd.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_types"] = CourseType.objects.all()
        context["courses"] = Course.objects.all()
        context["students"] = Student.objects.filter(is_deleted=0)
        return context


# 报名信息的编辑
class EditRegistrationView(LoginRequiredMixin, DetailView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    model = RegisterInfo
    template_name = "registration/regidtrationEdit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_info"] = RegisterInfo.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg),
                                                               is_deleted=0).first()
        context["students"] = Student.objects.filter(is_deleted=0)
        context["parent_courses"] = ParentCourse.objects.all()

        context["types"] = CourseType.objects.all()
        context["param_register"] = self.request.get_full_path()
        return context


# 报名信息编辑后进行保存
class EditRegistrationSaveView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        register_form = EditRegistrationForm(request.POST)
        if register_form.is_valid():
            register_hid_id = request.POST.get("register_hid_id", "")
            register_student_id = request.POST.get("register_student_id", "")
            register_course_id = request.POST.get("register_course_id", "")
            register_type_id = request.POST.get("register_type_id", "")
            register_hours = request.POST.get("register_hours", "")
            register_price = request.POST.get("register_price", "")
            register_discount = request.POST.get("register_discount", "")
            register_final_money = request.POST.get("register_final_money", "")
            register_date = request.POST.get("register_date", "")
            register_note = request.POST.get("register_note", "")
            register_info = RegisterInfo.objects.filter(pk=int(register_hid_id), is_deleted=0).first()
            register_info.course = Course.objects.filter(pk=int(register_course_id)).first()
            register_info.course_type = CourseType.objects.filter(pk=int(register_type_id)).first()
            register_info.student = Student.objects.filter(pk=int(register_student_id), is_deleted=0).first()
            register_info.hours = register_hours
            register_info.price = register_price
            register_info.discount = register_discount
            register_info.final_money = register_final_money
            register_info.register_date = register_date
            register_info.note = register_note
            register_info.save()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="修改"+register_info.student.name+"报名信息"
            )
            return JsonResponse({"status": "success"}, safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)


# ajax报名信息的添加
class AddRegistrationAjaxView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        student_id_str_list = json.loads(request.POST.get("student_id_list", ""))
        student_id_list = set([int(student_id) for student_id in student_id_str_list])
        register_course_id = request.POST.get("register_course_id", "")
        course_type_id = request.POST.get("course_type_id", "")
        register_hours = request.POST.get("hours", "")
        receivable = request.POST.get("receivable", "")
        discount = request.POST.get("discount", "")
        receipts = request.POST.get("receipts", "")
        register_date = request.POST.get("register_date", "")
        register_note = request.POST.get("register_note", "")
        for student_id in student_id_list:
            # 添加报名日志
            student=Student.objects.filter(id=student_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="添加" + student.name + "报名信息"
            )

            register = RegisterInfo(hours=register_hours, price=receivable, discount=discount, final_money=receipts,
                                    register_date=register_date, note=register_note, is_deleted=0)
            register.course = Course.objects.filter(pk=int(register_course_id)).first()
            register.course_type = CourseType.objects.filter(pk=int(course_type_id)).first()
            register.student = Student.objects.filter(pk=student_id).first()
            register.save()


        return JsonResponse({"status": "success"}, safe=False)


# 导出标准报名表
class UploadRegisterTableView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        f = create_registerinfo_excel_table()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % current_time
        f.save(response)
        return response


# 导出上课表
class UploadStudyInfoTableView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        f = create_studyinfo_excel_table()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % current_time
        f.save(response)
        return response


# 导出报名信息
class RegisterExcelCreateView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        excel_str_id_list = json.loads(self.request.POST.get("excel_id_list"))
        excel_id_list = [int(i) for i in excel_str_id_list]
        request.session["excel_id_list"] = excel_id_list
        return JsonResponse({"status": "success"}, safe=False)


# 导出报名信息
class RegisterExcelEmitView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        excel_id_list = request.session.get("excel_id_list", "")
        if "excel_id_list" in request.session.keys():
            del request.session['excel_id_list']
        if excel_id_list:
            emit_info = RegisterInfo.objects.filter(id__in=excel_id_list, is_deleted=0)
        else:
            emit_info = RegisterInfo.objects.filter(is_deleted=0)
        f = create_registerinfo_excel(emit_info)

        # 导出报名日志
        for register in emit_info:
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="导出" + register.student.name + "报名信息"
            )

        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % current_time
        f.save(response)
        return response


# 导入报名信息
class RegisterExcelImportView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        excel_form = UploadExcelForm(request.POST, request.FILES)
        if excel_form.is_valid():
            wb = xlrd.open_workbook(
                filename=None, file_contents=request.FILES['excel'].read())  # 关键点在于这里
        else:
            msg = "请选择要导入的Excel表"
            return JsonResponse({
                'status': 'error',
                'msg': msg
            })
        table = wb.sheets()[0]
        table_num = table.nrows
        register_info_list = []
        for i in range(1, table_num):
            data = table.row_values(i)

            try:
                if not data[0] or not data[1] or not data[2] or not data[3] or not data[4] or not data[5] or not data[
                    6] or data[7] == "" or data[8] == "" or data[9] == "" or data[10] == "":
                    msg = "第" + str(i + 1) + "行数据不能为空！，导入失败！"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })

                course_result = Course.objects.filter(course_name=data[5],
                                                      parent_name=ParentCourse.objects.filter(
                                                          name__icontains=re.match(r"\D+", data[5]).group()).first())
                if course_result.count() < 1:
                    msg = "第" + str(i) + "行" + data[5] + "课程不存在，导入失败!"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })
                course_type_result = CourseType.objects.filter(type_name=data[6])
                if course_type_result.count() < 1:
                    msg = "第" + str(i) + "行" + data[6] + "课程类型不存在，导入失败!"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })

                student_result = Student.objects.filter(name=data[2], first_name=data[0], last_name=data[1],
                                                        phone=self._to_int(data[3]))
                if student_result.count() < 1:
                    student = Student(name=data[2], first_name=data[0], last_name=data[1], phone=self._to_int(data[3]))
                    student.save()

                single_register_info = RegisterInfo.objects.filter(
                    hours=self._to_int(data[7]),
                    student=Student.objects.filter(name=data[2], first_name=data[0], last_name=data[1],
                                                   phone=self._to_int(data[3])).first(),
                    course=Course.objects.filter(course_name=data[5],
                                                 parent_name=ParentCourse.objects.filter(
                                                     name__icontains=re.match(r"\D+",
                                                                              data[5]).group()).first()).first(),
                    course_type=CourseType.objects.filter(type_name=data[6]).first(),
                    register_date=xlrd.xldate.xldate_as_datetime(data[4], 0),
                    price=Decimal(data[8]).quantize(Decimal('0.00')),
                    discount=Decimal(data[9]).quantize(Decimal('0.00')),
                    final_money=Decimal(data[10]).quantize(Decimal('0.00')),
                )
                if single_register_info.count() >= 1:
                    msg = "第" + str(i + 1) + "行报名信息已存在！，导入失败！"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })
                else:
                    single_register_info = RegisterInfo(
                        hours=self._to_int(data[7]),
                        student=Student.objects.filter(name=data[2], first_name=data[0], last_name=data[1],
                                                       phone=self._to_int(data[3])).first(),
                        course=Course.objects.filter(course_name=data[5],
                                                     parent_name=ParentCourse.objects.filter(
                                                         name__icontains=re.match(r"\D+",
                                                                                  data[5]).group()).first()).first(),
                        course_type=CourseType.objects.filter(type_name=data[6]).first(),
                        register_date=xlrd.xldate.xldate_as_datetime(data[4], 0),
                        price=Decimal(data[8]).quantize(Decimal('0.00')),
                        discount=Decimal(data[9]).quantize(Decimal('0.00')),
                        final_money=Decimal(data[10]).quantize(Decimal('0.00')),
                        note=data[11],
                    )
                    register_info_list.append(single_register_info)
            except:
                return JsonResponse({
                    'status': 'error',
                    'msg': '导入失败，请核查导入的表是否正确！'
                })

        RegisterInfo.objects.bulk_create(register_info_list)

        for register_info in register_info_list:
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="导入"+register_info.student.name+"报名信息"
            )
        msg = "导入成功！"
        return JsonResponse({
            'status': 'ok',
            'msg': msg
        })

    @staticmethod
    def _to_int(text):
        try:
            i = int(text)
        except ValueError:
            return text

        if i == text:
            return i
        else:
            return text


# 操作日志
class SignalListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = "signal.html"
    paginate_by = 8
    context_object_name = "signals"

    def get_queryset(self):
        if self.request.user.is_superuser:
            data_list=Oplog.objects.filter()
        else:
            data_list=Oplog.objects.filter(admin=self.request.user)
        return data_list


# 按条件查询日志
class SignalConditionSearchView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    template_name = 'signal.html'
    paginate_by = 8
    context_object_name = "signals"

    def get_queryset(self):
        operator_type = self.request.GET.get("operator_type", "")
        operator_time = self.request.GET.get("operator_time", "")
        # operator_type 0-全部，1-删除，2-添加，3-修改
        # operator_time 0-全部，1-今天，2-昨天，3-本周，4-上周，5-本月，6-上月
        today = datetime.date.today()  # 获得今天的日期
        yesterday = today - datetime.timedelta(days=1)  # 获得昨天的日期
        # weekday = today - datetime.timedelta(days=7)  # 获得本周的日期

        monday = today - datetime.timedelta(days=today.weekday())
        last_monday = monday - datetime.timedelta(days=7)
        last_sunday = monday - datetime.timedelta(days=1)

        firstday = today - datetime.timedelta(days=(today.day - 1))

        last_month_lastday = firstday - datetime.timedelta(days=1)
        last_month_firstday = datetime.date(last_month_lastday.year, last_month_lastday.month, 1)

        if int(operator_type) == 0:
            type_condition = ""
        elif int(operator_type) == 1:
            type_condition = "删除"
        elif int(operator_type) == 2:
            type_condition = "添加"
        elif int(operator_type) == 3:
            type_condition = "修改"
        elif int(operator_type) == 4:
            type_condition = "导入"
        elif int(operator_type) == 5:
            type_condition = "导出"
        elif int(operator_type) == 6:
            type_condition = "登入"
        elif int(operator_type) == 7:
            type_condition = "登出"
        elif int(operator_type) == 8:
            type_condition = "禁用"
        elif int(operator_type) == 9:
            type_condition = "还原"

        # reason__icontains = type_condition
        if self.request.user.is_superuser:
            if int(operator_time) == 0:
                data_list = Oplog.objects.filter(reason__icontains=type_condition)
            elif int(operator_time) == 1:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=today.year,
                                                 op_time__month=today.month,
                                                 op_time__day=today.day
                                                 )
            elif int(operator_time) == 2:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=yesterday.year,
                                                 op_time__month=yesterday.month,
                                                 op_time__day=yesterday.day,
                                                 )
            elif int(operator_time) == 3:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=monday.year,
                                                 op_time__month=monday.month,
                                                 op_time__day__range=(monday.day, today.day)
                                                 )
            elif int(operator_time) == 4:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=last_monday.year,
                                                 op_time__month=last_monday.month,
                                                 op_time__day__range=(last_monday.day, last_sunday.day)
                                                 )
            elif int(operator_time) == 5:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=firstday.year,
                                                 op_time__month=firstday.month,
                                                 op_time__day__range=(firstday.day, today.day)
                                                 )
            elif int(operator_time) == 6:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=last_month_firstday.year,
                                                 op_time__month=last_month_firstday.month,
                                                 op_time__day__range=(last_month_firstday.day, last_month_lastday.day)
                                                 )

        else:
            if int(operator_time) == 0:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,admin=self.request.user)
            elif int(operator_time) == 1:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=today.year,
                                                 op_time__month=today.month,
                                                 op_time__day=today.day,
                                                 admin=self.request.user
                                                 )
            elif int(operator_time) == 2:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=yesterday.year,
                                                 op_time__month=yesterday.month,
                                                 op_time__day=yesterday.day,
                                                 admin=self.request.user
                                                 )
            elif int(operator_time) == 3:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=monday.year,
                                                 op_time__month=monday.month,
                                                 op_time__day__range=(monday.day, today.day),
                                                 admin=self.request.user
                                                 )
            elif int(operator_time) == 4:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=last_monday.year,
                                                 op_time__month=last_monday.month,
                                                 op_time__day__range=(last_monday.day, last_sunday.day),
                                                 admin=self.request.user
                                                 )
            elif int(operator_time) == 5:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=firstday.year,
                                                 op_time__month=firstday.month,
                                                 op_time__day__range=(firstday.day, today.day),
                                                 admin=self.request.user
                                                 )
            elif int(operator_time) == 6:
                data_list = Oplog.objects.filter(reason__icontains=type_condition,
                                                 op_time__year=last_month_firstday.year,
                                                 op_time__month=last_month_firstday.month,
                                                 op_time__day__range=(last_month_firstday.day, last_month_lastday.day),
                                                 admin=self.request.user
                                                 )


        return data_list



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["param_signal"] = self.request.path
        return context
