from django.shortcuts import render, redirect
from django.http import HttpResponse
from committee.models import ScholarshipApplication
from .models import EligibilityCheck

def index(response, app_id=None):
    if app_id:
        app = ScholarshipApplication.objects.filter(id=app_id).first()
    else:
        app = ScholarshipApplication.objects.first()
    
    eligibility = None
    if app:
        eligibility, created = EligibilityCheck.objects.get_or_create(application=app)

        if response.method == "POST":
            eligibility.citizenship_check = response.POST.get('citizenship_check') == 'on'
            eligibility.programme_level_check = response.POST.get('programme_level_check') == 'on'
            
            eligibility.exam_foundation_spm = response.POST.get('exam_foundation_spm') == 'on'
            eligibility.exam_degree_stpm_uec = response.POST.get('exam_degree_stpm_uec') == 'on'
            eligibility.exam_degree_matriculation = response.POST.get('exam_degree_matriculation') == 'on'
            
            eligibility.grade_spm = response.POST.get('grade_spm') == 'on'
            eligibility.grade_stpm = response.POST.get('grade_stpm') == 'on'
            eligibility.grade_uec = response.POST.get('grade_uec') == 'on'
            eligibility.grade_foundation = response.POST.get('grade_foundation') == 'on'
            
            eligibility.documents_verified = response.POST.get('documents_verified') == 'on'
            eligibility.save()
            return redirect('reviewer_with_id', app_id=app.id)

    return render(response, "reviewer/reviewer.html", {'app': app, 'eligibility': eligibility})

def review(response):
    return render(response, "reviewer/reviewScholarship.html", {})

def details(response):
    return render(response, "reviewer/reviewScholarship.html", {})