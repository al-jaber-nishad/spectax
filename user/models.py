from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def user_directory_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.firstname + instance.lastname
    filename = name + '.' + ext
    return 'media/Faculty_Images/{}'.format(filename)


class Faculty(models.Model):
    is_teacher = (
        ('Teacher', True),
        ('Student', False),
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    is_teacher = models.CharField(
        max_length=100, default=True, choices=is_teacher)

    def __str__(self):
        return str(self.firstname + " " + self.lastname)


def student_directory_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.roll
    filename = name + '.' + ext
    return 'media/Student_Images/{}/{}'.format(instance.session, filename)


class Student(models.Model):
    SESSION_ = (
        ('2017-18', '2017-18'),
        ('2018-19', '2018-19'),
        ('2019-20', '2019-20'),
        ('2020-21', '2020-21'),
        ('2021-22', '2021-22'),
    )
    is_teacher = (
        ('Teacher', True),
        ('Student', False),
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    roll = models.CharField(max_length=200, null=True)
    session = models.CharField(max_length=100, null=True, choices=SESSION_)
    profile_pic = models.ImageField(
        upload_to=student_directory_path, null=True, blank=True)
    is_teacher = models.CharField(
        max_length=100, default=False, choices=is_teacher)

    def __str__(self):
        return str(self.roll)
