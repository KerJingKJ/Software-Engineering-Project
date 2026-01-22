from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


from .models import Application
from .forms import ApplicationForm



def index(request):
    return render(request, "student/student.html", {})

def scholarship_list(request):
    return render(request, "student/scholarshipList.html", {})

def scholarship_details(request):
    return render(request, "student/scholarshipDetails.html", {})

def bookmark_scholarship(request):
    return render(request, "student/bookmarkScholarship.html", {})

def eligibility(request):
    return render(request, "student/eligibility.html", {})

def application_form(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("applicationForm_p2")
        else:
            print(form.errors)
    else:
        form = ApplicationForm()


    return render(request, "student/applicationForm.html", {})

def application_form_p2(request):
    return render(request, "student/applicationForm_p2.html", {})

def application_form_p3(request):
    return render(request, "student/applicationForm_p3.html", {})

def application_form_p4(request):
    return render(request, "student/applicationForm_p4.html", {})

def application_form_status(request):
    return render(request, "student/applicationForm_status.html", {})

def track(request):
    return render(request, "student/trackApplication.html", {})


