from django.contrib import admin
from .models import Course, CourseType
from .models import Course,ParentCourse, CourseType

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseType)
admin.site.register(ParentCourse)
