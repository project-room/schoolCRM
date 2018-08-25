# _*_ coding: utf-8 _*_
_author__ = 'Aaron'
__time__ = '2018/4/19'

from django import forms
from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


# 登录表单验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


# 重置密码
class ModifyPwdForm(forms.Form):
    ori_pwd = forms.CharField(required=True, min_length=6)
    new_pwd = forms.CharField(required=True, min_length=6)
    ack_pwd = forms.CharField(required=True, min_length=6)


def validate_excel(value):
    if value.name.split('.')[-1] not in ['xls', 'xlsx']:
        raise ValidationError(_('Invalid File Type: %(value)s'), params={'value': value}, )


# 导入excel
class UploadExcelForm(forms.Form):
    excel = forms.FileField(validators=[validate_excel], error_messages={"invalid": "上传文件格式错误错误"})  # 这里使用自定义的验证


class UserAddForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"required": "该字段不能为空"})
    pwd = forms.CharField(required=True, min_length=6, error_messages={"min_length": "最短为6个字符", "required": "该字段不能为空"})
    ack_pwd = forms.CharField(required=True, min_length=6,
                              error_messages={"min_length": "最短为6个字符", "required": "该字段不能为空"})
    real_name = forms.CharField(required=True)
    # must_change_pwd = forms.BooleanField(required=True)



#编辑上课信息
class EditStudyInfoForm(forms.Form):
    studyinfo_course=forms.IntegerField(required=True)
    course_type_name=forms.IntegerField(required=True)
    studyinfo_hours = forms.IntegerField(required=True)
    studyinfo_class_date=forms.DateTimeField(required=True)
    study_student_id=forms.IntegerField(required=True)
    study_teacher_id=forms.IntegerField(required=True)

#添加课程
class AddBaseCourseForm(forms.Form):
    parent_course_name=forms.CharField(required=True)


#添加课程类型
class AddCourseTypeForm(forms.Form):
    add_course_type=forms.CharField(required=True)

#编辑报名信息
class EditRegistrationForm(forms.Form):
    register_student_id=forms.IntegerField(required=True)
    register_course_id=forms.IntegerField(required=True)
    register_type_id=forms.IntegerField(required=True)
    register_hours = forms.IntegerField(required=True)
    register_price=forms.DecimalField(required=True)
    register_discount=forms.DecimalField(required=True)
    register_final_money=forms.DecimalField(required=True)
    register_date=forms.DateTimeField(required=True)




