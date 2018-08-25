"""schoolCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from operators.views import LoginIndexView, LogOutView
from django.views.generic import TemplateView
from .views import StudentListView, StudentSearchView, StudentEditView, StudentAddView, StudentInfoView, \
    StudentAddSaveView, DeleteStudentInfoView, StudentEditSaveView, DeleteStudentInfoBatchView, StudentExcelCreateView, \
    StudentExcelEmitView, StudentExcelImportView, StudentSearchByNameAjaxView, UploadStudentTableView

urlpatterns = [
    url('^$', StudentListView.as_view(), name="student"),
    url(r'^search_stu/$', StudentSearchView.as_view(), name="search_stu"),
    url('info/(?P<pk>\d+)/$', StudentInfoView.as_view(), name="student_info"),
    url(r'^edit_stu/$', StudentEditView.as_view(), name="edit_stu"),
    url('add/$', StudentAddView.as_view(), name="student_add"),
    url('student_add_save/$', StudentAddSaveView.as_view(), name="student_add_save"),
    url('student_edit_save/$', StudentEditSaveView.as_view(), name="student_edit_save"),
    url('deletestudentinfo/$', DeleteStudentInfoView.as_view(), name="deletestudentinfo"),
    url('delete_studentinfo_batch/$', DeleteStudentInfoBatchView.as_view(), name="delete_studentinfo_batch"),
    url('stu_excel_out/$', StudentExcelCreateView.as_view(), name="stu_excel_out"),
    url('stu_excel_emit/$', StudentExcelEmitView.as_view(), name="stu_excel_emit"),
    url('stu_excel_import/$', StudentExcelImportView.as_view(), name="stu_excel_import"),
    url(r'^studyinfo_search_name/$', StudentSearchByNameAjaxView.as_view(), name="studyinfo_search_name"),
    url(r'^upload_student_table/$', UploadStudentTableView.as_view(), name="upload_student_table"),

]
