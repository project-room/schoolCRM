# _*_ coding: utf-8 _*_
from decimal import Decimal

from my_signals.oplog_signal import op_log
from operators.models import RegisterInfo, Oplog
from student.models import Student

_author__ = 'Aaron'
__time__ = '2018/4/21'

import xlwt


def create_courseinfo_excel(emit_info):
    column_names = ["Course", "Date", "Name", "LN", "FN", "Phone", "Hours", "Course Type", "Employee", "# Employee Name"]
    # 转化日期
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy/mm/dd'

    f = xlwt.Workbook()

    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)

    # TODO 下载excel逻辑
    for i in range(len(column_names)):
        sheet1.write(0, i, column_names[i])
        for j in range(len(emit_info)):  # 1 - 3
            sheet1.write(j + 1, 0, emit_info[j].course.course_name)
            sheet1.write(j + 1, 1, emit_info[j].class_date, dateFormat)
            sheet1.write(j + 1, 2, emit_info[j].student.name)
            sheet1.write(j + 1, 3, emit_info[j].student.last_name)
            sheet1.write(j + 1, 4, emit_info[j].student.first_name)
            sheet1.write(j + 1, 5, emit_info[j].student.phone)
            sheet1.write(j + 1, 6, emit_info[j].hours)
            sheet1.write(j + 1, 7, emit_info[j].course_type.type_name)
            sheet1.write(j + 1, 8, emit_info[j].teacher.employee_num)
            sheet1.write(j + 1, 9, emit_info[j].teacher.name)
    return f


def create_student_excel(emit_info):
    column_names = ["Name", "FN", "LN", "Phone"]
    # 转化日期
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy/mm/dd'

    f = xlwt.Workbook()

    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)

    # TODO 下载excel逻辑
    for i in range(len(column_names)):
        sheet1.write(0, i, column_names[i])
        for j in range(len(emit_info)):  # 1 - 3
            sheet1.write(j + 1, 0, emit_info[j].name)
            sheet1.write(j + 1, 1, emit_info[j].first_name)
            sheet1.write(j + 1, 2, emit_info[j].last_name)
            sheet1.write(j + 1, 3, emit_info[j].phone)
    return f


def create_teacher_excel(emit_info):
    column_names = ["Name", "FN", "LN", "Employee#", "Phone"]
    # 转化日期
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy/mm/dd'

    f = xlwt.Workbook()

    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)

    # TODO 下载excel逻辑
    for i in range(len(column_names)):
        sheet1.write(0, i, column_names[i])
        for j in range(len(emit_info)):
            sheet1.write(j + 1, 0, emit_info[j].name)
            sheet1.write(j + 1, 1, emit_info[j].first_name)
            sheet1.write(j + 1, 2, emit_info[j].last_name)
            sheet1.write(j + 1, 3, emit_info[j].employee_num)
            sheet1.write(j + 1, 4, emit_info[j].phone)
    return f

def create_registerinfo_excel(emit_info):
    column_names = ["FN", "LN", "Name", "Phone", "Date", "Course", "Type", "Hours", "price", "discount","final_money","note"]
    # 转化日期
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy/mm/dd'

    f = xlwt.Workbook()

    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)

    # TODO 下载excel逻辑
    for i in range(len(column_names)):
        sheet1.write(0, i, column_names[i])
        for j in range(len(emit_info)):  # 1 - 3
            sheet1.write(j + 1, 0, emit_info[j].student.first_name)
            sheet1.write(j + 1, 1, emit_info[j].student.last_name)
            sheet1.write(j + 1, 2, emit_info[j].student.name)
            sheet1.write(j + 1, 3, emit_info[j].student.phone)
            sheet1.write(j + 1, 4, emit_info[j].register_date, dateFormat)
            sheet1.write(j + 1, 5, emit_info[j].course.course_name)
            sheet1.write(j + 1, 6, emit_info[j].course_type.type_name)
            sheet1.write(j + 1, 7, emit_info[j].hours)
            sheet1.write(j + 1, 8, emit_info[j].price)
            sheet1.write(j + 1, 9, emit_info[j].discount)
            sheet1.write(j + 1, 10, emit_info[j].final_money)
            sheet1.write(j + 1, 11, emit_info[j].note)
    return f


#导出报名标准表
def create_registerinfo_excel_table():
    # column_names = ["FN", "LN", "Name", "Date", "Course", "Type", "Hours", "price", "discount", "final_money", "note"]

    f = xlwt.Workbook()
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)


    sheet1.write(0, 0, "FN")
    sheet1.write(0, 1, "LN")
    sheet1.write(0, 2, "Name")
    sheet1.write(0, 3, "Phone")
    sheet1.write(0, 4, "Date")
    sheet1.write(0, 5, "Course")
    sheet1.write(0, 6, "Type")
    sheet1.write(0, 7, "Hours")
    sheet1.write(0, 8, "price")
    sheet1.write(0, 9, "discount")
    sheet1.write(0, 10, "final_money")
    sheet1.write(0, 11, "note")
    return f

#导出上课标准表
def create_studyinfo_excel_table():
    # column_names = ["Course", "Date", "Name", "LN", "FN", "Phone", "Hours", "Course Type", "Employee", "# Employee Name"]

    f = xlwt.Workbook()
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)


    sheet1.write(0, 0, "Course")
    sheet1.write(0, 1, "Date")
    sheet1.write(0, 2, "Name")
    sheet1.write(0, 3, "LN")
    sheet1.write(0, 4, "FN")
    sheet1.write(0, 5, "Phone")
    sheet1.write(0, 6, "Hours")
    sheet1.write(0, 7, "Course Type")
    sheet1.write(0, 8, "Employee")
    sheet1.write(0, 9, "# Employee Name")
    return f

#导出学生标准表
def create_student_excel_table():
    # column_names = ["Name", "FN", "LN", "Phone"]

    f = xlwt.Workbook()
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "Name")
    sheet1.write(0, 1, "FN")
    sheet1.write(0, 2, "LN")
    sheet1.write(0, 3, "Phone")
    return f

#导出教师标准表
def create_teacher_excel_table():
    # column_names = ["Name", "FN", "LN", "Employee#", "Phone"]

    f = xlwt.Workbook()
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "Name")
    sheet1.write(0, 1, "FN")
    sheet1.write(0, 2, "LN")
    sheet1.write(0, 3, "Employee#")
    sheet1.write(0, 4, "Phone")
    return f