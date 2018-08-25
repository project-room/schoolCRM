import datetime
import json

import math
import xlrd
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# django_pure_pagination里面的模块
from pure_pagination.mixins import PaginationMixin

from my_signals.oplog_signal import op_log
from operators.forms import UploadExcelForm
from operators.models import CourseInfo, Oplog, RegisterInfo
from django.urls import reverse

from student.forms import AddStudentForm, EditStudentForm
from utils.excel_tool import create_courseinfo_excel, create_student_excel, create_student_excel_table
from .models import Student
import time
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.hashers import make_password


# Create your views here.


class StudentListView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    queryset = Student.objects.filter(is_deleted=0)
    template_name = 'student/student.html'
    paginate_by = 8


#学生条件查询
class StudentSearchView(LoginRequiredMixin, PaginationMixin, ListView):
    login_url = '/log_in/'
    redirect_field_name = 'next'
    paginate_by = 8
    template_name = 'student/student.html'

    def get_queryset(self):
        stu_name = self.request.GET.get("stu_name", "")
        data_list=Student.objects.filter(is_deleted=0)
        if stu_name:
            data_list=data_list.filter(Q(name__icontains=stu_name))
        return data_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["param_stu_search"] = self.request.path
        return context



# 通过学生名字来查找学生
class StudentSearchByNameAjaxView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        student_search_name = request.POST.get("student_search_name", "")
        if not student_search_name:
            students = Student.objects.filter(is_deleted=0)
            student_list=[]
            for student in students:
                student_info={}
                student_info["Name"]=student.name
                student_info["FN"]=student.first_name
                student_info["LN"]=student.last_name
                student_list.append(student_info)
            context={
                "status": "success",
                "students": student_list
            }
            return JsonResponse(context, safe=False)

        else:
            students = Student.objects.filter(Q(name__icontains=student_search_name), is_deleted=0)
            student_list = []
            for student in students:
                student_info = {}
                student_info["id"]=student.id
                student_info["Name"] = student.name
                student_info["FN"] = student.first_name
                student_info["LN"] = student.last_name
                student_list.append(student_info)
            context = {
                "status": "success",
                "students": student_list
            }
            return JsonResponse(context, safe=False)

class StudentInfoView(LoginRequiredMixin, DetailView):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    template_name = "student/studentDetail.html"
    context_object_name = "student_info"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_course_infos"] = CourseInfo.objects.filter(student__id=self.kwargs.get(self.pk_url_kwarg), is_deleted=0)
        context["student_register_infos"] = RegisterInfo.objects.filter(student__id=self.kwargs.get(self.pk_url_kwarg), is_deleted=0)
        context["param_stu"] = self.request.get_full_path()
        return context

    def get_queryset(self):
        student = Student.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg), is_deleted=0)
        return student


class StudentEditView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        student_id = request.POST.get("student_id")
        if student_id:
            student_info = Student.objects.filter(id=int(student_id), is_deleted=0).first()
            context = {}
            context["status"]="success"
            context["id"] = student_info.id
            context["name"] = student_info.name
            context["FN"] = student_info.first_name
            context["LN"] = student_info.last_name
            context["Phone"] = student_info.phone
            return JsonResponse(context, safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)


class StudentAddView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, "student/student_add.html")


class StudentAddSaveView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        student_add_form= AddStudentForm(request.POST)
        if student_add_form.is_valid():
            Name = request.POST.get("Name", "")
            FN = request.POST.get("FN", "")
            LN = request.POST.get("LN", "")
            Phone = request.POST.get("Phone", "")
            student=Student.objects.create(name=Name, first_name=FN, last_name=LN, phone=Phone)
            context = {
                "status": "success",
                "stu_id": student.id,
                "stu_Name": student.name,
                "stu_FN": student.first_name,
                "stu_LN": student.last_name,
            }
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="添加"+Name+"学生"
            )
            return JsonResponse(context, safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)





class StudentEditSaveView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        student_form=EditStudentForm(request.POST)
        if student_form.is_valid():
            student_id = request.POST.get("student_id", "")
            Name = request.POST.get("student_name", "")
            FN = request.POST.get("student_FN", "")
            LN = request.POST.get("student_LN", "")
            phone = request.POST.get("student_phone", "")
            Student.objects.filter(pk=int(student_id)).update(name=Name, first_name=FN, last_name=LN, phone=phone)
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="修改" + Name + "学生"
            )
            return JsonResponse({"status": "success"},safe=False)
        else:
            return JsonResponse({"status": "fail"}, safe=False)


class DeleteStudentInfoView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        student_id=request.POST.get("stu_id","")
        if student_id:
            Student.objects.filter(id=int(student_id)).update(is_deleted=1, delete_date=datetime.date.today())
            context={}
            context["status"] = "success"
            return JsonResponse(context, safe=False)
        else:
            return JsonResponse({"status":"fail"}, safe=False)

class DeleteStudentInfoBatchView(LoginRequiredMixin,View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        checkbox_list = request.POST.getlist("hxy")
        for student_info_id in checkbox_list:
            Student.objects.filter(id=student_info_id).update(is_deleted=1, delete_date=datetime.date.today())

            student=Student.objects.filter(id=student_info_id).first()
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="删除" +student.name+ "学生"
            )
        return HttpResponseRedirect(reverse('student'))

#导出学生
class StudentExcelCreateView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def post(self, request):
        excel_str_id_list = json.loads(self.request.POST.get("excel_id_list"))
        excel_id_list = [int(i) for i in excel_str_id_list]
        request.session["excel_id_list"] = excel_id_list
        return JsonResponse({"status": "success"}, safe=False)

#导出学生
class StudentExcelEmitView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):
        excel_id_list = request.session.get("excel_id_list", "")
        if "excel_id_list" in request.session.keys():
            del request.session['excel_id_list']
        if excel_id_list:
            emit_info = Student.objects.filter(id__in=excel_id_list, is_deleted=0)
        else:
            emit_info = Student.objects.filter(is_deleted=0)
        f = create_student_excel(emit_info)

        # 导出学生日志
        for student in emit_info:
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="导出" + student.name + "学生信息"
            )

        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % current_time
        f.save(response)
        return response

#导入学生
class StudentExcelImportView(View):
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
        student_info_list = []
        for i in range(1, table_num):
            data = table.row_values(i)

            try:
                if not data[0] or not data[1] or not data[2] or not data[3]:
                    msg = "第" + str(i + 1) + "行数据不能为空！，导入失败！"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })
                single_student=Student.objects.filter(name=data[0], first_name=data[1], last_name=data[2], phone=str(self._to_int(data[3])))
                if single_student.count()>=1:
                    msg = "第" + str(i + 1) + "行" + data[0] + ":学生已存在！，导入失败！"
                    return JsonResponse({
                        'status': 'error',
                        'msg': msg
                    })

                else:
                    single_student = Student(name=data[0], first_name=data[1], last_name=data[2], phone=str(self._to_int(data[3])))
                    student_info_list.append(single_student)
            except:
                msg = "导入失败，请核查导入的表是否正确！"
                return JsonResponse({
                    'status': 'error',
                    'msg': msg
                })

        Student.objects.bulk_create(student_info_list)

        for student_info in student_info_list:
            op_log.send(
                sender=Oplog,
                admin=request.user,
                reason="导入"+student_info.name+"学生信息"
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


#导出标准学生表
class UploadStudentTableView(View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):

        f = create_student_excel_table()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % current_time
        f.save(response)
        return response