from django.shortcuts import render, redirect
from attendance.models import Attendance
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from base.models import CustomUser, Courses

# Create your views here.


def teacher_dashboard(request):

  student_id = request.GET.get('student_id')
  session = request.GET.get('session')
  course = request.GET.get('course')
  period = request.GET.get('period')

  attendance = Attendance.objects.all()

  present = attendance.filter(status="Present").count()
  absent = attendance.filter(status="Absent").count()




  if student_id:
      attendance = attendance.filter(Student_ID=student_id)

  if session:
      attendance = attendance.filter(session=session)

  if course:
      attendance = attendance.filter(course=course)

  if period:
      attendance = attendance.filter(period=period)

  total = 0
  for item in attendance:
    total = total + item.attentiveness
  percentage = total / attendance.count()

  context = {
      'attendance': attendance,
      'present': present,
      'absent': absent,
      'percentage': percentage
  }
  
  return render(request, 'teacher/teacher-dashboard.html', context)


def create_class(request):

  return render(request, 'teacher/class/create-class.html')


# Student section
def student_add(request):
  if request.method == 'POST':
    # Get the form data from the request
    username = request.POST['username']
    name = request.POST['name']
    password = request.POST['password']
    email = request.POST['email']
    roll = request.POST['roll']
    session = request.POST['session']
    profile_pic = request.FILES.get('profile_pic')

    # Create a new CustomUser object
    CustomUser = get_user_model()
    custom_user = CustomUser.objects.create_user(username=username, password=password, email=email)
    custom_user.name = name
    custom_user.roll = roll
    custom_user.session = session
    custom_user.is_staff = False
    custom_user.profile_pic = profile_pic
    custom_user.save()

    # Redirect to a success page or any other desired page
    return redirect('student-list')  # Replace 'success' with the URL or view name for the success page

    # Render the create student template for GET requests
  return render(request, 'teacher/student/add.html')

def student_list(request):

  students = CustomUser.objects.filter(is_staff=False)

  context = {
    "students": students, 
  }

  return render(request, 'teacher/student/list.html', context)

# Courses Section
def courses_add(request):

  return render(request, 'teacher/courses/add.html')

def courses_list(request):

  courses = Courses.objects.all()

  context = {
    "courses": courses
  }

  return render(request, 'teacher/courses/list.html', context)

# Events
def events(request):

  return render(request, 'teacher/events.html')

# Settings
def settings(request):

  return render(request, 'teacher/settings.html')
