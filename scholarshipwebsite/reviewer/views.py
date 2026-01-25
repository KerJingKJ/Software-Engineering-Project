from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
 
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count
from committee.models import Scholarship
from student.models import Student, Application

# from committee.models import ScholarshipApplication
from student.models import Application
from student.models import Student, Application, ScholarshipApplication
from .models import EligibilityCheck

def review(response, app_id=None):
    if app_id:
        app = Application.objects.filter(id=app_id).first()
    else:
        app = Application.objects.first()
    
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
            
            # Qualitative Scoring Matrix - A. Academic Excellence
            eligibility.academic_borderline = response.POST.get('academic_borderline') == 'on'
            eligibility.academic_competent = response.POST.get('academic_competent') == 'on'
            eligibility.academic_superior = response.POST.get('academic_superior') == 'on'
            eligibility.academic_elite = response.POST.get('academic_elite') == 'on'
            
            # Qualitative Scoring Matrix - B. Academic Rigor & Awards
            eligibility.rigor_best_student = response.POST.get('rigor_best_student') == 'on'
            eligibility.rigor_competitions = response.POST.get('rigor_competitions') == 'on'
            eligibility.rigor_none = response.POST.get('rigor_none') == 'on'
            
            # Qualitative Scoring Matrix - B. Co-Curricular & Leadership
            eligibility.leadership_leader = response.POST.get('leadership_leader') == 'on'
            eligibility.leadership_subleader = response.POST.get('leadership_subleader') == 'on'
            eligibility.leadership_secretary = response.POST.get('leadership_secretary') == 'on'
            eligibility.leadership_committee = response.POST.get('leadership_committee') == 'on'
            eligibility.leadership_member = response.POST.get('leadership_member') == 'on'
            
            # B. Co-Curricular & Leadership - 2) Competition/Event Achievement
            eligibility.competition_national = response.POST.get('competition_national') == 'on'
            eligibility.competition_state = response.POST.get('competition_state') == 'on'
            eligibility.competition_university = response.POST.get('competition_university') == 'on'
            eligibility.competition_participant = response.POST.get('competition_participant') == 'on'
            
            # C. Personal Statement / Essay Quality
            eligibility.essay_compelling = response.POST.get('essay_compelling') == 'on'
            eligibility.essay_generic = response.POST.get('essay_generic') == 'on'
            eligibility.essay_poor = response.POST.get('essay_poor') == 'on'
            
            eligibility.save()
            return redirect('review_step2', app_id=app.id)

    return render(response, "reviewer/reviewScholarship.html", {'app': app, 'eligibility': eligibility})


def review_step2(response, app_id):
    app = ScholarshipApplication.objects.filter(id=app_id).first()
    eligibility, created = EligibilityCheck.objects.get_or_create(application=app)
    print(f"DEBUG: Eligibility={eligibility}, Integrity={getattr(eligibility, 'integrity_income_check', 'MISSING')}")
    
    if response.method == "POST":
        eligibility.integrity_income_check = response.POST.get('integrity_income_check') == 'on'
        
        eligibility.financial_priority = response.POST.get('financial_priority')
        
        eligibility.hardship_single_income = response.POST.get('hardship_single_income') == 'on'
        eligibility.hardship_large_family = response.POST.get('hardship_large_family') == 'on'
        eligibility.hardship_retiree = response.POST.get('hardship_retiree') == 'on'
        eligibility.hardship_medical = response.POST.get('hardship_medical') == 'on'
        
        eligibility.save()
        # Redirect case:
        if 'previous' in response.POST:
             return redirect('reviewer_with_id', app_id=app.id)
        else:
             # Next button was clicked
             # Ideally redirect to Step 3, but for now we can stay or go back to dashboard/step 3 placeholder
             # Since User said "Step 3 not done", let's redirect to a placeholder Step 3 or back to Step 2 for now.
             # Or better, create a temporary Step 3 view/url.
             # For this task, let's redirect to a simple "Done" or stay on Step 2 with a success message?
             # The user flow is Step 1 -> Step 2 -> Step 3.
             # I'll redirect to a "step 3" URL that I haven't implemented yet? 
             # No, better to redirect to a simple valid placeholder. 
             # For now, let's assume there is a step 3 coming. I'll make a dummy redirect or just refresh.
             # Actually, user said "Step 3 will have a save button".
             # I will redirect to a placeholder step 3 route.
             return redirect('review_step3', app_id=app.id)

    context = {
        'app': app,
        'eligibility': eligibility,
        'guardians': app.guardians.all(),
        'integrity_checked': getattr(eligibility, 'integrity_income_check', False),
        'financial_priority': getattr(eligibility, 'financial_priority', None),
        'hardship_single': getattr(eligibility, 'hardship_single_income', False),
        'hardship_large': getattr(eligibility, 'hardship_large_family', False),
        'hardship_retiree': getattr(eligibility, 'hardship_retiree', False),
        'hardship_medical': getattr(eligibility, 'hardship_medical', False),
    }
    return render(response, "reviewer/review_step2.html", context)

def review_step3(response, app_id):
      app = ScholarshipApplication.objects.filter(id=app_id).first()
      return HttpResponse("<h1>Step 3: Personal Statement / Essay Quality (Coming Soon)</h1>")


def details(response):
    return render(response, "reviewer/reviewScholarship.html", {})

def index(response):
    return render(response, "reviewer/reviewer.html", {})


## using rest_framework classes
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
                     "labels":labels,
                     "chartLabel":chartLabel,
                     "chartdata":chartdata,
             }
        return Response(data)