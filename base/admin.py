from django.contrib import admin
from .models import CustomUser, Courses
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Courses)