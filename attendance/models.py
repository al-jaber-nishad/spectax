from django.db import models

# Create your models here.

class Attendance(models.Model):
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    class_time = models.DateTimeField(auto_now_add=True, null = True)
    session = models.CharField(max_length=200, null = True)
    course = models.CharField(max_length=50, null= True)
    period = models.CharField(max_length=200, null = True)
    status = models.CharField(max_length=200, null = True, default='Absent')
    attentiveness = models.IntegerField()

    def __str__(self):
        return f"{self.Student_ID}_{self.period}"


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

