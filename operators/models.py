from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.datetime_safe import datetime

from student.models import Student
from teacher.models import Teacher
from course.models import Course, CourseType, ParentCourse


# Create your models here.
class UserProfile(AbstractUser):
    real_name = models.CharField(max_length=10, verbose_name="真实姓名")
    must_change_pwd = models.SmallIntegerField(default=0, verbose_name="下次登录是否修改密码", choices=((0, "是"), (1, "否")))
    is_deleted = models.PositiveSmallIntegerField(default=0, choices=((0, "正常数据"), (1, "放入回收站数据"), (2, "彻底被删除数据")))


    class Meta:
        verbose_name = "操作人员"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# 上课信息
class CourseInfo(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程名")
    course_type = models.ForeignKey(CourseType, verbose_name="课程类型")
    student = models.ForeignKey(Student, verbose_name="选修该课程的学生")
    teacher = models.ForeignKey(Teacher, verbose_name="该课程的任课老师")
    hours = models.IntegerField(null=False, blank=False, default=0, verbose_name="上课时长")
    remaining_time = models.IntegerField(default=0, verbose_name="剩余课时")
    class_date = models.DateField(verbose_name="上课时间")
    is_deleted = models.PositiveSmallIntegerField(default=0, choices=((0, "正常数据"), (1, "放入回收站数据"), (2, "彻底被删除数据")))
    delete_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "上课信息"
        verbose_name_plural = verbose_name
        ordering=["-class_date"]

    def __str__(self):
        return self.course.course_name

# 报名信息
class RegisterInfo(models.Model):
    student = models.ForeignKey(Student, verbose_name="选修该课程的学生")
    # max_digits，小数总长度
    # decimal_places，小数位长度
    course = models.ForeignKey(Course, verbose_name="课程名")
    course_type = models.ForeignKey(CourseType, verbose_name="课程类型")
    hours = models.IntegerField(null=False, blank=False, default=0, verbose_name="报名时长")

    # TODO 修改max_digits的值
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="应收金额")
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="折扣")
    final_money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="实收金额")
    register_date = models.DateField(null=True, blank=True, verbose_name="注册日期")
    note = models.CharField(max_length=255, verbose_name="备注")
    is_deleted = models.PositiveSmallIntegerField(default=0, choices=((0, "正常数据"), (1, "放入回收站数据"), (2, "彻底被删除数据")))
    delete_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name="报名信息"
        verbose_name_plural=verbose_name
        ordering = ["-register_date"]

    def __str__(self):
        return self.student.name + self.course.course_name

class Oplog(models.Model):
    admin = models.ForeignKey(UserProfile, verbose_name="管理员")
    reason = models.CharField(max_length=255, verbose_name="操作原因")
    op_time = models.DateTimeField(default=datetime.now, verbose_name="操作时间")
    class Meta:
        verbose_name = "操作日志记录"
        verbose_name_plural = verbose_name
        ordering = ["-op_time"]
    def __str__(self):
        return self.op_time.strftime("%Y-%m-%d %X") + self.admin.real_name + self.reason
