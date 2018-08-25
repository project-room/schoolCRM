from django.db import models
from course.models import Course, ParentCourse


# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=10, verbose_name="教师姓名")
    first_name = models.CharField(max_length=10, verbose_name="名")
    last_name = models.CharField(max_length=10, verbose_name="姓")
    #联系方式
    phone = models.CharField(max_length=225, verbose_name="手机号码")
    # employee_num = models.PositiveIntegerField()
    employee_num=models.CharField(max_length=10, verbose_name="教工编号")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    course = models.ManyToManyField(Course, verbose_name="课程名")
    #父课程
    parent_course=models.ManyToManyField(ParentCourse, verbose_name="父课程名")
    is_deleted = models.PositiveSmallIntegerField(default=0, choices=((0, "正常数据"), (1, "放入回收站数据"), (2, "彻底被删除数据")))
    delete_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name
        ordering=['-add_time']
        # index_together = ("name", "course")  # 联合索引

    def __str__(self):
        return self.name
