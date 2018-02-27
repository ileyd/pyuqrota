"""
A python API client for the University of Queensland's Rota timetabling sysem
"""

from .courses import Course, courses_by_criteria
from .semesters import Semester, get_all_semesters