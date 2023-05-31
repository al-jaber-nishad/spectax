from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    # Add your additional fields here
    # Example:
    roll = models.CharField(max_length=200)
    session = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Specify any additional fields or behaviors you need for your custom user model

    def __str__(self):
        return self.username


class Courses(models.Model):
  course_name = models.CharField(max_length=255)
  course_code = models.CharField(max_length=255)
  total_classes = models.IntegerField()

  def __str__(self):
    return f"{self.course_name}"



class Event(models.Model):
  pass  


