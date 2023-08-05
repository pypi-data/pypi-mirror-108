# -*- coding:utf-8 -*-

from .u_student import U_Student
from .constant import Student_Type


def get_student(stutype: Student_Type=Student_Type.UNDERGRADUATE) -> U_Student:
    if stutype == Student_Type.UNDERGRADUATE:
        return U_Student()
    else:
        return None
