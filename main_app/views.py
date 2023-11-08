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
    data = Student.objects.all()
    random_value = datetime.now().timestamp()*random.randint(10000, 100000)
    print(str(random_value))
    return render(request, "display.html", {"students": data})


def details(request, student_id):
    student = Student.objects.get(pk=student_id)  # SELECT * FROM students WHERE id=1
    return render(request, "details.html", {"student": student})
