from django.shortcuts import render,redirect
from .models import Student
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
import csv
# Create your views here.

def index(request,pk):
    students = Student.objects.get(id=pk)
    return render(request, 'home.html',{'student':students})

def index2(request):
    course_query = request.GET.get('course', '')
    if course_query:
        student_list = Student.objects.filter(course__icontains=course_query).order_by('name')
    else:
        student_list = Student.objects.all().order_by('name')

    paginator = Paginator(student_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'student': page_obj.object_list,
        'course_query': course_query
    }
    return render(request, 'home2.html', context)


def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        course = request.POST.get('course')
        obj = Student(name=name,email=email,age=age,course=course)
        obj.save()
        return redirect('home0')
    
def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')
        # Check if email is used
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1,first_name=first_name,last_name=last_name)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    return render(request, 'signup.html')

def student_delete(request,pk):
    student = Student.objects.get(id=pk)
    student.delete()
    return redirect('home0')

def login_user(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=un, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                messages.success(request, 'Admin Login successful!')
                return redirect('home0')
            else:
                messages.success(request, 'Login successful!')
                return redirect('home2')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

def student_edit(request,pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.age = request.POST.get('age')
        student.course = request.POST.get('course')
        student.save()
        return redirect('home0')
    return render(request,'edit.html',{'student':student})

def index0(request):
    course_query = request.GET.get('course', '')  # Get 'course' from query params
    if course_query:
        student_list = Student.objects.filter(course__icontains=course_query).order_by('name')
    else:
        student_list = Student.objects.all().order_by('name')

    paginator = Paginator(student_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    course_distribution = list(Student.objects.values('course').annotate(count=Count('course')))
    context = {
        'page_obj': page_obj,
        'student': page_obj.object_list,
        'course_query': course_query,  # pass it to template to keep input value
        'course_distribution': course_distribution
    }
    return render(request, 'home0.html', context)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Age', 'Course', 'Added On'])

    students = Student.objects.all().values_list('id', 'name', 'email', 'age', 'course', 'created_at')
    for student in students:
        writer.writerow(student)

    return response