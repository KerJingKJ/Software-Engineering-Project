from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(response):
    return render(response, "reviewer/reviewer.html", {})

def review(response):
    return render(response, "reviewer/reviewScholarship.html", {})