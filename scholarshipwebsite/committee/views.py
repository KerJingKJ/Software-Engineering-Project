from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ScholarshipForm
from .models import Scholarship, Interview, ApprovedApplication
from student.models import Application, Guardian, Notification
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
    approved = Application.objects.filter(committee_status='Approved').count()
    rejected = Application.objects.filter(committee_status='Rejected').count()
    pending = Application.objects.exclude(committee_status__in=['Approved', 'Rejected']).count()
    
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

def reviewApprove(request):
    if request.user.is_authenticated:
        applications = Application.objects.filter(reviewer_status = 'Reviewed', assigned_committee_member=request.user).order_by('submitted_date')
    else:
        # Fallback for anonymous access (local dev)
        applications = Application.objects.filter(reviewer_status = 'Reviewed').order_by('submitted_date')

    for app in applications:
        # Determine display status based on session or DB
        app.interview_scheduled = Interview.objects.filter(application=app).exists()

        if app.committee_status == 'Approved':
            app.dashboard_status = 'Approved'
            app.dashboard_class = 'approved'
        elif app.committee_status == 'Rejected':
            app.dashboard_status = 'Rejected'
            app.dashboard_class = 'rejected'
        
        else:
            app.dashboard_status = 'Pending Review'
            app.dashboard_class = 'pending-review'
    
    return render(request, "committee/reviewApprove.html", {"applications": applications})

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

        # Check if the time slot is already taken by another application
        conflict = Interview.objects.filter(date=date, interview_time=interview_time).exclude(application=application).exists()
        
        if conflict:
            messages.error(request, f"The time slot {interview_time} on {date} is already taken. Please choose another time.")
            return render(request, "committee/schedule_interview.html", {
                'application': application,
                'existing_interview': existing_interview,
                'is_scheduled': existing_interview is not None
            })

        interview, created = Interview.objects.update_or_create(
            application=application,
            defaults={
                'date': date,
                'interview_time': interview_time,
                'timezone': timezone,
            }
        )
        
        if request.user.is_authenticated:
            interview.committee = request.user
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
        location = request.POST.get('location')
        remarks = request.POST.get('remarks')
        
        if interview:
            interview.location = location
            interview.remarks = remarks
            interview.save()

        if decision == 'Approved':
            application.committee_status = 'Approved'
            application.save()
            
            Notification.objects.create(
                student=application.student,
                message=f"Congratulations! Your application for {application.scholarship.name} has been APPROVED."
            )
            
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
            return redirect('reviewApprove')
        elif decision == 'Rejected':
            application.committee_status = 'Rejected'
            application.save()
            
            Notification.objects.create(
                student=application.student,
                message=f"Update on your application: Your application for {application.scholarship.name} was REJECTED."
            )
            
            ApprovedApplication.objects.filter(original_application=application).delete()

            # Interview.objects.filter(application=application).delete() # Keep interview record but set status
            
            return redirect('reviewApprove')
            
    return render(request, "committee/decision.html", {'application': application, 'interview': interview})

from reviewer.models import EligibilityCheck

def view_reviewer_mark(request, id):
    application = get_object_or_404(Application, pk=id)
    eligibility = EligibilityCheck.objects.filter(application=application).first()
    interview = Interview.objects.filter(application=application).first()
    
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'approve':
            application.committee_status = 'Approved'
            application.save()
            
            # Create or update ApprovedApplication
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
            messages.success(request, f"Application for {application.name} has been approved.")
            return redirect('reviewApprove')
            
        elif action == 'reject':
            application.committee_status = 'Rejected'
            application.save()
            # Clean up approved record if it exists
            ApprovedApplication.objects.filter(original_application=application).delete()
            
            messages.warning(request, f"Application for {application.name} has been rejected.")
            return redirect('reviewApprove')

    # Prepare list of "checked" items for display
    checked_items = []
    if eligibility:
        field_labels = {
            'citizenship_check': 'Citizenship Verified',
            'programme_level_check': 'Programme Level Verified',
            'exam_foundation_spm': 'Qualifying Exam: Foundation/SPM',
            'exam_degree_stpm_uec': 'Qualifying Exam: STPM/UEC',
            'exam_degree_matriculation': 'Qualifying Exam: Matriculation',
            'grade_spm': 'Minimum Grade: SPM',
            'grade_stpm': 'Minimum Grade: STPM',
            'grade_uec': 'Minimum Grade: UEC',
            'grade_foundation': 'Minimum Grade: Foundation',
            'documents_verified': 'All Documents Verified',
            'academic_borderline': 'Academic: Borderline',
            'academic_competent': 'Academic: Competent',
            'academic_superior': 'Academic: Superior',
            'academic_elite': 'Academic: Elite',
            'rigor_best_student': 'Academic Rigor: Best Student',
            'rigor_competitions': 'Academic Rigor: Competition Winner',
            'leadership_leader': 'Leadership: President/Captain',
            'leadership_subleader': 'Leadership: Vice President/Vice Captain',
            'leadership_secretary': 'Leadership: Secretary/Treasurer',
            'leadership_committee': 'Leadership: Committee Member',
            'leadership_member': 'Leadership: Active Member',
            'competition_national': 'Competition: National Level',
            'competition_state': 'Competition: State Level',
            'competition_university': 'Competition: University Level',
            'competition_participant': 'Competition: School/Club Level',
            'essay_compelling': 'Essay: Compelling',
            'essay_generic': 'Essay: Generic/Satisfactory',
            'essay_poor': 'Essay: Poor',
            'integrity_income_check': 'Financial Integrity Verified',
            'hardship_single_income': 'Hardship: Single Income Parent',
            'hardship_large_family': 'Hardship: Large Family (>4 kids)',
            'hardship_retiree': 'Hardship: Retired/Pensioner Parent',
            'hardship_medical': 'Hardship: Chronic Medical Condition',
        }
        
        for field, label in field_labels.items():
            if getattr(eligibility, field, False):
                checked_items.append(label)
        
        if eligibility.financial_priority:
            priority_display = dict(EligibilityCheck.FINANCIAL_PRIORITY_CHOICES).get(eligibility.financial_priority)
            checked_items.append(f"Financial Need: {priority_display}")

    return render(request, "committee/view_reviewer_mark.html", {
        'application': application,
        'eligibility': eligibility,
        'checked_items': checked_items
    })

 

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