from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(response):
    return render(response, "committee/committee.html", {})

def manage(response):
    return render(response, "committee/manageScholarship.html", {})

def create(response):
    return render(response, "committee/createScholarship.html", {})

def edit(response):
    return render(response, "committee/editScholarship.html", {})

def reviewApprove(response):
    return render(response, "committee/reviewApprove.html", {})

def schedule(response):
    return render(response, "committee/scheduleInterview.html", {})