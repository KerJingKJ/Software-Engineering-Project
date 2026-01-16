from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ScholarshipForm
from .models import Scholarship, ScholarshipApplication, Guardian, Interview, ApprovedApplication

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

def view_application_details(request, id):
    application = get_object_or_404(ScholarshipApplication, pk=id)
    return render(request, "committee/application_details_review.html", {'application': application})

def view_family_background(request, id):
    application = get_object_or_404(ScholarshipApplication, pk=id)
    guardians = application.guardians.all()
    return render(request, "committee/family_background_review.html", {'application': application, 'guardians': guardians})

def schedule_interview(request, id):
    application = get_object_or_404(ScholarshipApplication, pk=id)
    
    if request.method == "POST":
        date = request.POST.get('date')
        interview_time = request.POST.get('interview_time')
        timezone = request.POST.get('timezone')
        
        # Check if interview already exists, update it; otherwise create new
        interview, created = Interview.objects.get_or_create(
            application=application,
            defaults={
                'date': date,
                'interview_time': interview_time,
                'timezone': timezone,
            }
        )
        if not created:
            # Update existing interview
            interview.date = date
            interview.interview_time = interview_time
            interview.timezone = timezone
        # If user is logged in, assign as reviewer
        if request.user.is_authenticated:
            interview.reviewer = request.user
        interview.save()
        
        return redirect('decision_page', id=id)

    return render(request, "committee/schedule_interview.html", {'application': application})

def decision_page(request, id):
    application = get_object_or_404(ScholarshipApplication, pk=id)
    interview = Interview.objects.filter(application=application).first()
    
    if request.method == "POST":
        decision = request.POST.get('decision')
        if decision == 'Approved':
            application.status = 'Approved'
            application.save()
            
            # Copy data to ApprovedApplication table
            if interview:
                ApprovedApplication.objects.update_or_create(
                    original_application=application,
                    defaults={
                        'scholarship_name': application.scholarship.name,
                        'student_name': application.name,
                        'ic_no': application.ic_no,
                        'email_address': application.email_address,
                        'contact_number': application.contact_number,
                        'programme': application.programme,
                        'interview_date': interview.date,
                        'interview_time': interview.interview_time,
                        'interview_timezone': interview.timezone,
                        'approved_by': request.user if request.user.is_authenticated else None
                    }
                )
            return redirect('decision_page', id=id)
        elif decision == 'Rejected':
            application.status = 'Rejected'
            application.save()
            
            # Remove from ApprovedApplication if exists (reversing approval)
            ApprovedApplication.objects.filter(original_application=application).delete()
            
            # Remove from Interview if exists
            Interview.objects.filter(application=application).delete()
            
            return redirect('decision_page', id=id)
            
    return render(request, "committee/decision.html", {'application': application, 'interview': interview})