# Generated by Django 4.0.1 on 2023-01-22 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_attendence_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('session', models.CharField(max_length=200, null=True)),
                ('course', models.CharField(max_length=50, null=True)),
                ('period', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(default='Absent', max_length=200, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Attendence',
        ),
    ]