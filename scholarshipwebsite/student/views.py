from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


from .models import Application
from .forms import ApplicationForm



def index(response):
    return render(response, "student/student.html", {})

def scholarship_list(response):
    return render(response, "student/scholarshipList.html", {})

def scholarship_details(response):
    return render(response, "student/scholarshipDetails.html", {})

def bookmark_scholarship(response):
    return render(response, "student/bookmarkScholarship.html", {})

def eligibility(response):
    return render(response, "student/eligibility.html", {})

def application_form(response):
    return render(response, "student/applicationForm.html", {})

def application_form_p2(response):
    return render(response, "student/applicationForm_p2.html", {})

def application_form_p3(response):
    return render(response, "student/applicationForm_p3.html", {})

def application_form_p4(response):
    return render(response, "student/applicationForm_p4.html", {})

def application_form_status(response):
    return render(response, "student/applicationForm_status.html", {})

def track(response):
    return render(response, "student/trackApplication.html", {})


