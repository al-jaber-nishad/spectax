from django.shortcuts import render, redirect
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from django.contrib.auth.decorators import login_required
from .models import Attendance, Image
from .serializers import ImageSerializer

from .filters import AttendanceFilter
# from user.models import Student
# from .recognizer2 import Recognizer2
from datetime import date
import os
from djqscsv import render_to_csv_response
from django.conf import settings
from pathlib import Path
import random

# Create your views here.



from .recognizer import predict




@csrf_exempt
def image_upload_view(request):
    if request.method == 'POST':

        image = request.FILES.get('image')
        session = request.POST.get('session')
        course_name = request.POST.get('course')
        period = request.POST.get('period')

        if image:
            image_data = {'image': image}
            serializer = ImageSerializer(data=image_data)
            if serializer.is_valid():
                # Save the image
                saved_image_path = default_storage.save(image.name, image)
                print("Image is received!!!", saved_image_path)
                absolute_image_path = os.path.join(settings.MEDIA_ROOT, saved_image_path)
                print(absolute_image_path)

                # Process the image
                recognized_person = predict(absolute_image_path)

                # Create a new instance of the RecognizedFace model
                if recognized_person is not None and session != None and course_name != None and period != None:
                    attentiveness = random.randint(70, 90)
                    recognized_face = Attendance(Student_ID=recognized_person, session=session, course=course_name, period=period, status='Present', attentiveness=attentiveness)

                    existing_record = Attendance.objects.filter(Student_ID=recognized_person, session=session, course=course_name, period=period).exists()

                    if not existing_record:
                        recognized_face.save()

                # Delete the image
                default_storage.delete(saved_image_path)

                return JsonResponse(serializer.data, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'error': 'No image file received'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def std_attendance(request, pk):
    context = {

    }
    return render(request, "attendance/std_attendance.html", context)


def std_check_attendance(request, pk):

    attendances = Attendance.objects.filter(
        Student_ID=request.user.student.roll).order_by('-id')
    myFilter = AttendanceFilter(request.GET, queryset=attendances)
    attendances = myFilter.qs

    context = {
        "myFilter": myFilter,
        "attendances": attendances,
        "check": True
    }

    return render(request, "attendance/std_check_attendance.html", context)


# Take Attendance form here!
def tch_attendance(request):
    context = {

    }

    # return render(request, "attendance/tch_attendance.html", context)
    return render(request, "attendance/std_attendance.html", context)


def tch_check_attendance(request):

    attendances = Attendance.objects.all()
    myFilter = AttendanceFilter(request.GET, queryset=attendances)
    attendances = myFilter.qs

    context = {
        "myFilter": myFilter,
        "attendances": attendances,
        "check": True
    }

    return render(request, "attendance/tch_check_attendance.html", context)


@login_required(login_url='login')
def take_attendance(request):
    if request.method == 'POST':
        details = {
            'course': request.POST['course'],
            'session': request.POST['session'],
            'period': request.POST['period'],
        }

        students = Student.objects.filter(
            roll=request.user.student.roll)
        names = Recognizer(details)
        print("Names from views.py", names)
        for student in students:
            if Attendance.objects.filter(date=str(date.today()), session=details['session'], period=details['period'], Student_ID=str(student.roll), course=details['course']).count() != 0:
                messages.error(request, "Attendance already recorded.")
                return redirect('tch_attendance')

            elif str(student.roll) in names:
                attendance = Attendance(
                    Student_ID=str(
                        student.roll),
                    course=details['course'],
                    session=details['session'],
                    period=details['period'],
                    status='Present')
                attendance.save()
            else:
                attendance = Attendance(Student_ID=str(
                    student.roll),
                    course=details['course'],
                    session=details['session'],
                    period=details['period'])
                attendance.save()
        attendances = Attendance.objects.filter(date=str(date.today(
        )), session=details['session'], period=details['period'], course=details['course'])
        context = {"attendances": attendances, "check": False}
        messages.success(request, "Attendance is taken Successfully!")
        if request.user.is_staff:
            return render(request, 'attendance/tch_check_attendance.html', context)
        else:
            return render(request, 'attendance/std_check_attendance.html', context)

    context = {}
    return render(request, 'call/lobby.html', context)


def csv_view(request):
    attendances = Attendance.objects.filter(
        Student_ID=request.user.student.roll)

    return render_to_csv_response(attendances, delimiter='|')
