from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(response):
    return render(response, "committee/committee.html", {})

def manage(response):
    return render(response, "committee/manageScholarship.html", {})

def reviewApprove(response):
    return render(response, "committee/reviewApprove.html", {})