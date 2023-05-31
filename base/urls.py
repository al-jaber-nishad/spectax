from django.urls import path 
from base import views

urlpatterns = [
    # Teacher
    path('teacher/dashboard', views.teacher_dashboard, name="teacher-dashboard"),
    path('teacher/create-class', views.create_class, name="create_class"),
    # Student
    path('teacher/student-list', views.student_list, name="student-list"),
    path('teacher/student-add', views.student_add, name="student-add"),
    # Courses
    path('teacher/courses-list', views.courses_list, name="courses-list"),
    path('teacher/courses-add', views.courses_add, name="courses-add"),

    path('teacher/events', views.events, name="events"),

    path('teacher/settings', views.settings, name="settings"),

    # Student
]
