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
from django.conf.urls import url

from teacher.views import TeacherAddSaveView, TeacherListView, TeacherSearchView, TeacherInfoView, TeacherEditView, \
    TeacherAddView, TeacherEditSaveView, DeleteTeacherInfoByIdView, DeleteTeacherInfoBatchView, TeacherExcelCreateView, \
    TeacherExcelEmitView, TeacherExcelImportView, UploadTeacherTableView

urlpatterns = [
    url('^$', TeacherListView.as_view(), name="teacher"),
    url(r'^search_teacher/$', TeacherSearchView.as_view(), name="search_teacher"),
    url('info/(?P<pk>\d+)/$', TeacherInfoView.as_view(), name="teacher_info"),
    url('edit/$', TeacherEditView.as_view(), name="teacher_edit"),
    url('add/$', TeacherAddView.as_view(), name="teacher_add"),
    url('add_save/$', TeacherAddView.as_view(), name="teacher_add_save"),
    url('add_save_tea/$', TeacherAddSaveView.as_view(), name="add_save_tea"),
    url('teacher_edit_save/$', TeacherEditSaveView.as_view(), name="teacher_edit_save"),
    url(r'^deleteteacherinfo/$', DeleteTeacherInfoByIdView.as_view(), name="deleteteacherinfo"),
    url(r'^deleteteacherinfobatch/$', DeleteTeacherInfoBatchView.as_view(), name="deleteteacherinfobatch"),
    url(r'^teach_excel_out/$', TeacherExcelCreateView.as_view(), name="teach_excel_out"),
    url(r'^teach_excel_emit/$', TeacherExcelEmitView.as_view(), name="teach_excel_emit"),
    url(r'^teach_excel_import/$', TeacherExcelImportView.as_view(), name="teach_excel_import"),
    url(r'^upload_teacher_table/$', UploadTeacherTableView.as_view(), name="upload_teacher_table"),
]
