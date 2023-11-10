from django.contrib import messages
from django.core.paginator import Paginator
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
            messages.success(request, "Student saved successfully")
            # messages.error(request, "Error while saving the student")
            # messages.warning(request, "This action is going to delete your record")
            # messages.info(request, "Tomorrow will be a holiday, please check your calendar")
            return redirect("home")
    else:
        form = StudentForm()
    return render(request, "students.html", {"form": form})


def show_students(request):
    data = Student.objects.all()  # SELECT * FROM students
    # data = Student.objects.all().order_by("-kcpe_score")
    # data = Student.objects.filter(first_name="Gran")
    # data = Student.objects.filter(first_name__startswith="gr")
    # data = Student.objects.filter(first_name__icontains="GR")
    # data = Student.objects.filter(first_name__icontains="GR", last_name__icontains="c", kcpe_score__gt=250) # AND
    # data = Student.objects.filter(first_name__icontains="GR") | Student.objects.filter(last_name__icontains="La")
    # data = Student.objects.filter(dob__year=1997, dob__month=1)
    # today = datetime.today()
    # mon = today.month
    # day = today.day  #[0, 1, 2,3 ]
    # data = Student.objects.filter(dob__month=mon, dob__day=day).order_by("-first_name")
    paginator = Paginator(data, 15)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request, "display.html", {"students": data})


# show?page=1

def details(request, student_id):
    student = Student.objects.get(pk=student_id)  # SELECT * FROM students WHERE id=1
    return render(request, "details.html", {"student": student})


def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    messages.info(request, f"Student {student.first_name} {student.last_name} was deleted successfully")
    return redirect("show")


def students_search(request):
    search = request.GET["search"]
    data = Student.objects.filter(
        Q(first_name__icontains=search)
        | Q(last_name__icontains=search)
        | Q(email__icontains=search)
    )

    if search.isnumeric():
        score = int(search)
        data = Student.objects.filter(kcpe_score=score)

    paginator = Paginator(data, 15)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request, "display.html", {"students": data})


# Elastic search
def update_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)  # SELECT * FROM students WHERE id=1
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully updated student {student.first_name}")
            return redirect("details", student_id)
    else:
        form = StudentForm(instance=student)
    return render(request, "update.html", {"form": form})

# CRUD