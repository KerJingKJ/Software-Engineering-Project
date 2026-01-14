from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ScholarshipForm

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def create_scholarship(request):
    if request.method == "POST":
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Scholarship created successfully!")
    else:
        form = ScholarshipForm()
    
    return HttpResponse("This endpoint accepts POST requests to create scholarships.")

def index(response):
    return render(response, "committee/committee.html", {})

def manage(response):
    return render(response, "committee/manageScholarship.html", {})

def reviewApprove(response):
    return render(response, "committee/reviewApprove.html", {})