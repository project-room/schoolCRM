from django.db import models
from course.models import Course


# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=10, verbose_name="学生姓名")
    first_name = models.CharField(max_length=10, verbose_name="名")
    last_name = models.CharField(max_length=10, verbose_name="姓")
    #联系方式
    phone=models.CharField(max_length=225, verbose_name="手机号码")
    course = models.ManyToManyField(Course, verbose_name="课程名")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    is_deleted = models.PositiveSmallIntegerField(default=0, choices=((0, "正常数据"), (1, "放入回收站数据"), (2, "彻底被删除数据")))
    delete_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]
        ordering = ["-add_time"]

    def __str__(self):
        return self.name
