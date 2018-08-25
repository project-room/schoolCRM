from django import forms

#学生添加form
class AddStudentForm(forms.Form):
    Name=forms.CharField(required=True)
    FN=forms.CharField(required=True)
    LN=forms.CharField(required=True)
    Phone = forms.CharField(required=True)

#学生编辑form
class EditStudentForm(forms.Form):
    student_name = forms.CharField(required=True)
    student_FN = forms.CharField(required=True)
    student_LN = forms.CharField(required=True)
    student_phone = forms.CharField(required=True)
