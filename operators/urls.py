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
from django.views.generic import TemplateView
from .views import AccountView, StudyInfoTrashListView, StudentTrashListView, TeacherTrashListView, \
    PeopleTrashListView, StudyInfoTrashRedoView, StudyInfoTrashDeleteForeverView, StudentTrashDeleteForeverView, \
    TeacherInfoTrashDeleteForeverView, PeopleTrashDeleteForeverView, TeacherTrashRedoView, StudentTrashRedoView, \
    PeopleTrashRedoView, SettingsView, SettingsEditView, TopSettingsEditView, SettingsUserSearchView, \
    SettingsUserForbidView, SettingsUserAddView, SettingsUserAddSaveView, SettingsUserDeleteView, ModifyPwdView, \
    StudyInfoExcelEmitView, StudyInfoExcelImportView, StudyInfoView, StudyInfoSearchView, StudyInfoEditSaveView, \
    DeleteStudyInfoView, DeleteStudyInfoByIdView, RegistrationView, RegistrationDeleteView, RegistrationSearchView, \
    BaseSettingsView, AddBaseCourseView, AddCourseTypeView, SettingsUserEditSaveView, AddRegistrationView, \
    EditRegistrationView, AddRegistrationAjaxView, AddStudyInfoAjaxView, RegisterExcelCreateView, RegisterExcelEmitView, \
    RegisterExcelImportView, BaseSettingsDetail, BaseTypesDetail, BaseSettingsDelete, RegisterTrashListView, \
    RegisterTrashRedoView, RegisterInfoTrashDeleteForeverView, StudyInfoDetailView, EditRegistrationSaveView, \
    UpdateParentCourseNameView, UpdateChildrenCourseNameView, UpdateCourseTypeNameView, UploadRegisterTableView, \
    UploadStudyInfoTableView, GetParentCoursesView, GetBaseSettingTypeView, GetBaseSettingCourseView, SignalListView, \
    SignalConditionSearchView
from .views import AccountView, ModifyPwdView, StudyInfoExcelEmitView, StudyInfoExcelImportView, \
    StudyInfoTrashListView, StudentTrashListView, TeacherTrashListView, PeopleTrashListView, SettingsView, \
    SettingsEditView, StudyInfoView, \
    SettingsUserAddSaveView, StudyInfoSearchView, DeleteStudyInfoView, SettingsUserSearchView, SettingsUserForbidView, \
    SettingsUserAddView, \
    SettingsUserDeleteView, StudyInfoTrashRedoView, StudyInfoTrashDeleteForeverView, TeacherTrashRedoView, \
    StudentTrashRedoView, TopSettingsEditView, RegistrationView, BaseSettingsView, StudyInfoExcelCreateView

urlpatterns = [
    # url('^$', IndexView.as_view(), name="index"),
    url(r'^account/$', AccountView.as_view(), name="account"),

    url(r'^recycle/$', StudyInfoTrashListView.as_view(), name="recycle"),
    url(r'^recycle_student/$', StudentTrashListView.as_view(), name="recycle_stu"),
    url(r'^recycle_teacher/$', TeacherTrashListView.as_view(), name="recycle_teacher"),
    url(r'^recycle_people/$', PeopleTrashListView.as_view(), name="recycle_people"),
    url(r'^recycle_register/$', RegisterTrashListView.as_view(), name="recycle_register"),
    url(r'^redo_studyinfo/$', StudyInfoTrashRedoView.as_view(), name="redo_studyinfo"),

    # 下面这个是单条删除
    url(r'^redo_studyinfo_byid/$', StudyInfoTrashRedoView.as_view(), name="redo_studyinfo_byid"),

    url(r'^delete_studyinfo_forever/$', StudyInfoTrashDeleteForeverView.as_view(), name="delete_studyinfo_forever"),
    url(r'^delete_studyinfo_forever_byid/$', StudyInfoTrashDeleteForeverView.as_view(),
        name="delete_studyinfo_forever_byid"),
    url(r'^delete_studyinfo_forever_byid/$', StudyInfoTrashDeleteForeverView.as_view(), name="delete_studyinfo_forever_byid"),
    url(r'^student_trash_delete_forever/$', StudentTrashDeleteForeverView.as_view(), name="student_trash_delete_forever"),
    url(r'^teacher_info_trash_delete_forever/$', TeacherInfoTrashDeleteForeverView.as_view(), name="teacher_info_trash_delete_forever"),
    url(r'^register_info_trash_delete_forever/$', RegisterInfoTrashDeleteForeverView.as_view(), name="register_info_trash_delete_forever"),
    url(r'^people_trash_delete_forever/$', PeopleTrashDeleteForeverView.as_view(), name="people_trash_delete_forever"),
    url(r'^teachertrashredo/$', TeacherTrashRedoView.as_view(), name="teachertrashredo"),
    url(r'^studenttrashredo/$', StudentTrashRedoView.as_view(), name="studenttrashredo"),
    url(r'^peopletrashredo/$', PeopleTrashRedoView.as_view(), name="peopletrashredo"),
    url(r'^registertrashredo/$', RegisterTrashRedoView.as_view(), name="registertrashredo"),




    url(r'^settings/$', SettingsView.as_view(), name="settings"),
    url(r'^edit_settings/(?P<pk>\d+)/$', SettingsEditView.as_view(), name="edit_settings"),
    # 左上角编辑按钮 TODO 考虑是否把左上角和右边的编辑按钮进行一个统一
    url(r'^top_editsettings/$', TopSettingsEditView.as_view(), name="top_editsettings"),

    url(r'^search_user/$', SettingsUserSearchView.as_view(), name="search_user"),
    url(r'^forbid_user/$', SettingsUserForbidView.as_view(), name="forbid_user"),
    url(r'^add_user/$', SettingsUserAddView.as_view(), name="add_user"),

    url(r'^add_user_save/$', SettingsUserAddSaveView.as_view(), name="add_user_save"),
    url(r'^edit_user/$', SettingsUserEditSaveView.as_view(), name="edit_user"),
    url(r'^del_user/$', SettingsUserDeleteView.as_view(), name="del_user"),
    url(r'^del_user_byid/(?P<user_id>\d+)/$', SettingsUserDeleteView.as_view(), name="del_user_byid"),

    url(r'^modifypwd/$', ModifyPwdView.as_view(), name="modifypwd"),

    url(r'^emitcreateexcel/$', StudyInfoExcelCreateView.as_view(), name="emit_create_excel"),
    url(r'^emitexcel/$', StudyInfoExcelEmitView.as_view(), name="emit_excel"),
    url(r'^emit_create_excel_register/$', RegisterExcelCreateView.as_view(), name="emit_create_excel_register"),
    url(r'^emit_excel_register/$', RegisterExcelEmitView.as_view(), name="emit_excel_register"),
    url(r'^upload_register_table/$', UploadRegisterTableView.as_view(), name="upload_register_table"),
    url(r'^upload_studyinfo_table/$', UploadStudyInfoTableView.as_view(), name="upload_studyinfo_table"),

    url(r'^exceltestpage/$', TemplateView.as_view(template_name="excel_test.html"), name="exceltestpage"),

    url(r'^importexcel/$', StudyInfoExcelImportView.as_view(), name="emit_import"),
    url(r'^emit_import_register/$', RegisterExcelImportView.as_view(), name="emit_import_register"),

    url(r'^editstudyinfo/$', StudyInfoView.as_view(), name="editstudyinfo"),
    url(r'^searchstudyinfo/$', StudyInfoSearchView.as_view(), name="searchstudyinfo"),
    url(r'^study_info_edit_save/$', StudyInfoEditSaveView.as_view(), name="study_info_edit_save"),
    url(r'^deletestudyinfo/$', DeleteStudyInfoView.as_view(), name="deletestudyinfo"),
    url(r'^deletestudyinfobyid/$', DeleteStudyInfoByIdView.as_view(), name="deletestudyinfobyid"),
    url(r'^addstudyinfoajax/$', AddStudyInfoAjaxView.as_view(), name="addstudyinfoajax"),
    url(r'^study_info_detail/(?P<pk>\d+)/$', StudyInfoDetailView.as_view(), name="study_info_detail"),

    # registration
    url(r'^registration/$', RegistrationView.as_view(), name="registration"),
    url(r'^registration_delete/$', RegistrationDeleteView.as_view(), name='registration_delete'),
    url(r'^registration_search/$', RegistrationSearchView.as_view(), name='registration_search'),
    url(r'^registration_add/$', AddRegistrationView.as_view(), name='registration_add'),
    url(r'^registration_edit/(?P<pk>\d+)/$', EditRegistrationView.as_view(), name='registration_edit'),
    url(r'^addregistrationajax/$', AddRegistrationAjaxView.as_view(), name='addregistrationajax'),
    url(r'^edit_register_save/$', EditRegistrationSaveView.as_view(), name='edit_register_save'),
    # 基础设置
    url(r'^basesettings/$', BaseSettingsView.as_view(), name="basesettings"),
    url(r'^addbasecourse/$', AddBaseCourseView.as_view(), name="addbasecourse"),
    url(r'^coursetype/$', AddCourseTypeView.as_view(), name="coursetype"),
    url(r'^get_parent/$', GetParentCoursesView.as_view(), name="get_parent"),
    url(r'^base_detail/$', BaseSettingsDetail.as_view(), name="base_detail"),
    url(r'^base_type/$', BaseTypesDetail.as_view(), name="base_type"),
    url(r'^base_del/$', BaseSettingsDelete.as_view(), name="base_del"),
    url(r'^update_parent_course_name/$', UpdateParentCourseNameView.as_view(), name="update_parent_course_name"),
    url(r'^update_child_course_name/$', UpdateChildrenCourseNameView.as_view(), name="update_child_course_name"),
    url(r'^update_course_type_name/$', UpdateCourseTypeNameView.as_view(), name="update_course_type_name"),
    url(r'^get_course_types/$', GetBaseSettingTypeView.as_view(), name="get_course_types"),
    url(r'^get_courses/$', GetBaseSettingCourseView.as_view(), name="get_courses"),
    # 操作日志
    url(r'^get_signals/$', SignalListView.as_view(), name="get_signals"),
    url(r'^search_signal/$', SignalConditionSearchView.as_view(), name="search_signal"),

]
