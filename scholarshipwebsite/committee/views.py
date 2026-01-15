from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ScholarshipForm
from .models import Scholarship

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def create_scholarship(request):
    if request.method == "POST":
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage")
    else:
        form = ScholarshipForm()
    
    return render(request, "committee/create_scholarship.html", {'form': form})

@csrf_exempt
def edit_scholarship(request, id):
    scholarship = get_object_or_404(Scholarship, pk=id)
    if request.method == "POST":
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()
            return redirect("manage")
    else:
        form = ScholarshipForm(instance=scholarship)
    
    return render(request, "committee/create_scholarship.html", {'form': form})

@csrf_exempt
def delete_scholarship(request, id):
    scholarship = get_object_or_404(Scholarship, pk=id)
    if request.method == "POST":
        scholarship.delete()
        return redirect("manage")
    return redirect("manage")

def index(response):
    return render(response, "committee/committee.html", {})

def manage(response):
    scholarships = Scholarship.objects.all()
    return render(response, "committee/manageScholarship.html", {"scholarships": scholarships})

def reviewApprove(response):
    return render(response, "committee/reviewApprove.html", {})