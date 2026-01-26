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
            eligibility.save()
            return redirect('reviewer_with_id', app_id=app.id)

    return render(response, "reviewer/reviewScholarship.html", {'app': app, 'eligibility': eligibility})


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