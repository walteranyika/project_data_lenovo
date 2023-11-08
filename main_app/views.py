import random
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from main_app.app_forms import StudentForm
from main_app.models import Student


# Create your views here.
def students(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = StudentForm()
    return render(request, "students.html", {"form": form})


def show_students(request):
    # data = Student.objects.all() # SELECT * FROM students
    # data = Student.objects.all().order_by("-kcpe_score")
    # data = Student.objects.filter(first_name="Gran")
    # data = Student.objects.filter(first_name__startswith="gr")
    # data = Student.objects.filter(first_name__icontains="GR")
    # data = Student.objects.filter(first_name__icontains="GR", last_name__icontains="c", kcpe_score__gt=250) # AND
    # data = Student.objects.filter(first_name__icontains="GR") | Student.objects.filter(last_name__icontains="La")
    # data = Student.objects.filter(dob__year=1997, dob__month=1)
    today = datetime.today()
    mon = today.month
    day = today.day  #[0, 1, 2,3 ]
    data = Student.objects.filter(dob__month=mon, dob__day=day).order_by("-first_name")
    return render(request, "display.html", {"students": data})


def details(request, student_id):
    student = Student.objects.get(pk=student_id)  # SELECT * FROM students WHERE id=1
    return render(request, "details.html", {"student": student})


def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return redirect("show")