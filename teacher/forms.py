from django import forms


class AddTeacherForm(forms.Form):
    name=forms.CharField(required=True)
    FN=forms.CharField(required=True)
    LN = forms.CharField(required=True)
    emp=forms.CharField(required=True)
    phone=forms.CharField(required=True)

class EditTeacherForm(forms.Form):
    teacher_name=forms.CharField(required=True)
    FN=forms.CharField(required=True)
    LN=forms.CharField(required=True)
    teacher_num=forms.IntegerField(required=True)
    teacher_phone = forms.IntegerField(required=True)