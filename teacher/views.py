import json

import xlrd
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
# django_pure_pagination里面的模块
from pure_pagination.mixins import PaginationMixin

from my_signals.oplog_signal import op_log
from operators.forms import UploadExcelForm
from operators.models import CourseInfo, RegisterInfo, Oplog
from django.urls import reverse
from course.models import Course, ParentCourse
from student.models import Student
from teacher.forms import AddTeacherForm, EditTeacherForm
from utils.excel_tool import create_teacher_excel, create_student_excel_table, create_teacher_excel_table
from .models import Teacher
import datetime
import time
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.hashers import make_password


# Create your views here.

#教师信息列表
class TeacherListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    queryset = Teacher.objects.filter(is_deleted=0)
    template_name = 'teacher/teacher.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()
        context["parent_courses"]=ParentCourse.objects.all()
        return context


#教师个人详情
class TeacherInfoView(LoginRequiredMixin, DetailView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    template_name = "teacher/teacherDetail.html"
    context_object_name = "teacher_info"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teacher_course_infos"] = CourseInfo.objects.filter(teacher__id=self.kwargs.get(self.pk_url_kwarg),is_deleted=0)
        teacher=Teacher.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg), is_deleted=0).first()
        context["courses"]=teacher.course.all()
        context["param_teach"] = self.request.get_full_path()
        return context

    def get_queryset(self):
        teacher=Teacher.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg), is_deleted=0)
        return teacher


#教师条件查询
class TeacherSearchView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    paginate_by = 8
    template_name = 'teacher/teacher.html'

    def get_queryset(self):
        teacher_name = self.request.GET.get("teahcer_name", "")
        course_type_id = self.request.GET.get("course_type", "")
        data_list=Teacher.objects.filter(is_deleted=0)
        if teacher_name:
            data_list=data_list.filter(Q(name__icontains=teacher_name))
        if course_type_id:
            data_list=data_list.filter(course=Course.objects.filter(pk=int(course_type_id)).first())
        return data_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_courses"] = ParentCourse.objects.all()
        context["param_teach_search"] = self.request.path
        return context



class TeacherEditView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        teacher_id=request.POST.get("teacher_id","")
        teacher_info=Teacher.objects.filter(pk=teacher_id).first()
        context={}
        context["status"]="success"
        context["tea_id"] = teacher_info.id
        context["tea_name"]=teacher_info.name
        context["tea_FN"]=teacher_info.first_name
        context["tea_LN"]=teacher_info.last_name
        context["tea_num"]=teacher_info.employee_num
        tea_courses = []
        course_list = teacher_info.course.all()
        for course in course_list:
            tea_courses.append(course.course_name+"-"+str(course.id))
        context["courses"]=tea_courses




        return JsonResponse(context,safe=False)


class TeacherAddView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, "teacher/teacher_add.html")

# 添加教师
class TeacherAddSaveView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        teacher_form=AddTeacherForm(request.POST)
        if teacher_form.is_valid():
            Employee_num = request.POST.get("emp", "")
            teacher_num=Teacher.objects.filter(employee_num=Employee_num).first()
            if teacher_num:
                return JsonResponse({"status": "fail"}, safe=False)
            else:
                course_id_list_str=json.loads(request.POST.get("course_id_list",""))
                course_id_list = [int(course_id) for course_id in course_id_list_str]
                Name = request.POST.get("name", "")
                FN = request.POST.get("FN", "")
                LN = request.POST.get("LN", "")
                phone=request.POST.get("phone", "")
                teacher=Teacher(name=Name, first_name=FN, last_name=LN, employee_num=Employee_num, phone=phone)
                teacher.save()

                teacher.course.add(*course_id_list)
                context={}
                context["status"]= "success"

                op_log.send(
                    sender=Oplog,
                    admin=request.user,
                    reason="添加" + Name + "教师"
                )
                return JsonResponse({"status": "success"},safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)

class TeacherEditSaveView(LoginRequiredMixin,View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self,request):
        teacher_form=EditTeacherForm(request.POST)
        if teacher_form.is_valid():
            teacher_id=request.POST.get("teacher_id","")
            Name = request.POST.get("teacher_name", "")
            FN = request.POST.get("FN", "")
            LN = request.POST.get("LN", "")
            employeeNum = request.POST.get("teacher_num", "")
            phone = request.POST.get("teacher_phone", "")
            courses_int=[int(course_id) for course_id in request.POST.getlist('teacher_courses[]')]

            Teacher.objects.filter(pk=int(teacher_id)).update(name=Name, first_name=FN, last_name=LN,employee_num=employeeNum, phone=phone)
            teacher=Teacher.objects.filter(pk=teacher_id).first()

            teacher.course=courses_int
            teacher.save()

            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="修改" + Name + "教师"
            )
            return JsonResponse({"status":"success"},safe=False)
        else:
            return JsonResponse({"status":"fail"}, safe=False)


class DeleteTeacherInfoByIdView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        teacher_id=request.POST.get("teacher_id","")
        Teacher.objects.filter(id=teacher_id).update(is_deleted=1, delete_date=datetime.date.today())
        context={
            "status":"success"
        }
        return JsonResponse(context,safe=False)

class DeleteTeacherInfoBatchView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy")
        for teacher_info_id in checkbox_list:
            Teacher.objects.filter(id=teacher_info_id).update(is_deleted=1, delete_date=datetime.date.today())

            teacher=Teacher.objects.filter(id=teacher_info_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="删除" + teacher.name + "教师"
            )
        return HttpResponseRedirect(reverse("teacher"))

#导出教师
class TeacherExcelCreateView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        excel_str_id_list = json.loads(self.request.POST.get("excel_id_list"))
        excel_id_list = [int(i) for i in excel_str_id_list]
        request.session["excel_id_list"] = excel_id_list
        return JsonResponse({"status": "success"}, safe=False)

#导出教师
class TeacherExcelEmitView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        excel_id_list = request.session.get("excel_id_list", "")
        if "excel_id_list" in request.session.keys():
            del request.session['excel_id_list']
        if excel_id_list:
            emit_info = Teacher.objects.filter(id__in=excel_id_list, is_deleted=0)
        else:
            emit_info = Teacher.objects.filter(is_deleted=0)
        f = create_teacher_excel(emit_info)

        # 导出教师日志
        for teacher in emit_info:
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="导出" + teacher.name + "教师信息"
            )

        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % current_time
        f.save(response)
        return response

#导入教师
class TeacherExcelImportView(View):
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
        teacher_info_list = []
        for i in range(1, table_num):
            data = table.row_values(i)

            try:
                if not data[0] or not data[1] or not data[2] or not data[3] or not data[4]:
                    msg = "第"+str(i+1)+"行数据不能为空！，导入失败！"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })
                single_teacher = Teacher.objects.filter(name=data[0], first_name=data[1], last_name=data[2], employee_num=str(self._to_int(data[3])), phone=str(self._to_int(data[4])))
                if single_teacher.count() >= 1:
                    msg = "第"+str(i+1)+"行"+data[0]+":教师已存在！，导入失败！"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })
                else:
                    single_teacher = Teacher(name=data[0], first_name=data[1], last_name=data[2], employee_num=str(self._to_int(data[3])), phone=str(self._to_int(data[4])))
                    teacher_info_list.append(single_teacher)
            except:
                msg = "导入失败，请核查导入的表是否正确！"
                return JsonResponse({
                    'status': 'error',
                    'msg': msg
                })

        Teacher.objects.bulk_create(teacher_info_list)

        for teacher_info in teacher_info_list:
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="导入"+teacher_info.name+"教师信息"
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

#导出标准教师表
class UploadTeacherTableView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):

        f = create_teacher_excel_table()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % current_time
        f.save(response)
        return response
