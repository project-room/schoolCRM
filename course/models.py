from django.db import models


# Create your models here.


class ParentCourse(models.Model):
    name = models.CharField(max_length=20, verbose_name="父课程名")

    class Meta:
        verbose_name = "父课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Course(models.Model):
    course_name = models.CharField(max_length=20, verbose_name="子课程名")
    parent_name = models.ForeignKey(ParentCourse, verbose_name="父课程名")
    hours = models.CharField(max_length=10, verbose_name="课程时长")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course_name


class CourseType(models.Model):
    type_short = models.CharField(max_length=10, verbose_name="课程类型简写")
    type_name = models.CharField(max_length=10, verbose_name="课程类型名称")

    class Meta:
        verbose_name = "课程类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name
