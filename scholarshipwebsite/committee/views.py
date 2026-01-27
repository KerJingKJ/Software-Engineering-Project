from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ScholarshipForm
from .models import Scholarship, Interview, ApprovedApplication
from student.models import Application, Guardian
from .models import Scholarship#, ScholarshipApplication, Guardian, Interview, ApprovedApplication

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render
from django.views.generic import View
 
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count

from student.models import Student, Application, Guardian


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
    total_apps = Application.objects.count()
    approved = Application.objects.filter(status='Approved').count()
    rejected = Application.objects.filter(status='Rejected').count()
    pending = Application.objects.exclude(status__in=['Approved', 'Rejected']).count()
    
    context = {
        'total_apps': total_apps,
        'approved': approved,
        'rejected': rejected,
        'pending': pending
    }
    return render(response, "committee/committee.html", context)

def manage(response):
    scholarships = Scholarship.objects.all()
    return render(response, "committee/manageScholarship.html", {"scholarships": scholarships})

def manageAccount(response):
    return render(response, "committee/manage_account.html", {})

def create(response):
    return render(response, "committee/createScholarship.html", {})

def edit(response):
    return render(response, "committee/editScholarship.html", {})

def reviewApprove(response):
    applications = Application.objects.all().order_by('submitted_date')

    for app in applications:
        # Determine display status based on session or DB
        app.interview_scheduled = Interview.objects.filter(application=app).exists()

        if app.status == 'Approved':
            app.dashboard_status = 'Approved'
            app.dashboard_class = 'approved'
        elif app.status == 'Rejected':
            app.dashboard_status = 'Rejected'
            app.dashboard_class = 'rejected'
        
        else:
            app.dashboard_status = 'Pending Review'
            app.dashboard_class = 'pending-review'
    
    return render(response, "committee/reviewApprove.html", {"applications": applications})

def view_application_details(request, id):
    application = get_object_or_404(Application, pk=id)
    return render(request, "committee/application_details_review.html", {'application': application})

def view_family_background(request, id):
    application = get_object_or_404(Application, pk=id)
    guardians = []
    if application.guardian1:
        guardians.append(application.guardian1)
    if application.guardian2:
        guardians.append(application.guardian2)

    return render(request, "committee/family_background_review.html", {'application': application, 'guardians': guardians})

def schedule_interview(request, id):
    application = get_object_or_404(Application, pk=id)
    existing_interview = Interview.objects.filter(application=application).first()
    
    if request.method == "POST":
        date = request.POST.get('date')
        interview_time = request.POST.get('interview_time')
        timezone = request.POST.get('timezone')
        
        
        interview, created = Interview.objects.get_or_create(
            application=application,
            defaults={
                'date': date,
                'interview_time': interview_time,
                'timezone': timezone,
            }
        )
        if not created:
            
            interview.date = date
            interview.interview_time = interview_time
            interview.timezone = timezone
        
        if request.user.is_authenticated:
            interview.reviewer = request.user
        interview.save()
        
        return redirect('decision_page', id=id)

    return render(request, "committee/schedule_interview.html", {
        'application': application,
        'existing_interview': existing_interview,
        'is_scheduled': existing_interview is not None
        })

def decision_page(request, id):
    application = get_object_or_404(Application, pk=id)
    interview = Interview.objects.filter(application=application).first()
    
    if request.method == "POST":
        decision = request.POST.get('decision')
        if decision == 'Approved':
            application.status = 'Approved'
            application.save()
            
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
                        # 'timezone': interview.timezone,
                        # 'approver': request.user if request.user.is_authenticated else None
                    }
                )
            return redirect('decision_page', id=id)
        elif decision == 'Rejected':
            application.status = 'Rejected'
            application.save()

            ApprovedApplication.objects.filter(original_application=application).delete()

            Interview.objects.filter(application=application).delete()
            
            return redirect('decision_page', id=id)
            
    return render(request, "committee/decision.html", {'application': application, 'interview': interview})

 

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
 
    def get(self, request, format = None):
        scholarships = Scholarship.objects.annotate(
            app_count=Count('applications')
        )

        labels = [s.name for s in scholarships]
        chartLabel = "Scholarship Application Volume"
        chartdata = [s.app_count for s in scholarships]
        total_applications = Application.objects.count()
        data ={
            'labels': labels,
            'chartLabel': chartLabel,
            'chartdata': chartdata,
        }
        return Response(data)