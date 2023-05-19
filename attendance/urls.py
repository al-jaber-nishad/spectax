from django.urls import path
from . import views

urlpatterns = [
    path("my-attendance/<int:pk>/", views.std_attendance, name="std_attendance"),
    path("my-attendance/", views.tch_attendance, name="tch_attendance"),
    path("attendance/", views.take_attendance, name="takeattendance"),
    path("take-attendance/", views.std_attendance, name="take-attendance"),


    path("std-check-attendance/<int:pk>",
         views.std_check_attendance, name="std-check-attendance"),
    path("tch-check-attendance/", views.tch_check_attendance,
         name="tch-check-attendance"),

    path("download-csv", views.csv_view, name="download-csv"),

    path('api/upload-image/', views.image_upload_view, name='upload-image')

]
