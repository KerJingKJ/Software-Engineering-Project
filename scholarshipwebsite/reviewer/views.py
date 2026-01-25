from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count
from committee.models import Scholarship
from student.models import Student, Application, ScholarshipApplication
from .models import EligibilityCheck
from django.contrib import messages

def review(request, app_id=None):
    if app_id:
        app = ScholarshipApplication.objects.filter(id=app_id).first()
    else:
        app = ScholarshipApplication.objects.first()
    
    if not app:
        return redirect('reviewer')

    if request.method == "POST":
        data = request.session.get(f'review_{app.id}', {})
        
        step1_fields = [
            'citizenship_check', 'programme_level_check', 'exam_foundation_spm',
            'exam_degree_stpm_uec', 'exam_degree_matriculation', 'grade_spm',
            'grade_stpm', 'grade_uec', 'grade_foundation', 'documents_verified',
            'academic_borderline', 'academic_competent', 'academic_superior', 'academic_elite',
            'rigor_best_student', 'rigor_competitions', 'rigor_none',
            'leadership_leader', 'leadership_subleader', 'leadership_secretary',
            'leadership_committee', 'leadership_member', 'competition_national',
            'competition_state', 'competition_university', 'competition_participant'
        ]
        
        for f in step1_fields:
            data[f] = request.POST.get(f) == 'on'
        
        request.session[f'review_{app.id}'] = data
        messages.success(request, "Step 1 progress cached.")
        return redirect('review_step2', app_id=app.id)
    
    existing_data = request.session.get(f'review_{app.id}')
    if existing_data is None:
        ec = EligibilityCheck.objects.filter(application=app).first()
        if ec:
            existing_data = {f: getattr(ec, f) for f in [
                'citizenship_check', 'programme_level_check', 'exam_foundation_spm',
                'exam_degree_stpm_uec', 'exam_degree_matriculation', 'grade_spm',
                'grade_stpm', 'grade_uec', 'grade_foundation', 'documents_verified',
                'academic_borderline', 'academic_competent', 'academic_superior', 'academic_elite',
                'rigor_best_student', 'rigor_competitions', 'rigor_none',
                'leadership_leader', 'leadership_subleader', 'leadership_secretary',
                'leadership_committee', 'leadership_member', 'competition_national',
                'competition_state', 'competition_university', 'competition_participant'
            ]}
        else:
            existing_data = {}

    context = {
        'app': app,
        'data': existing_data,
        'c_attr': 'checked' if existing_data.get('citizenship_check') else '',
        'pl_attr': 'checked' if existing_data.get('programme_level_check') else '',
        'efs_attr': 'checked' if existing_data.get('exam_foundation_spm') else '',
        'eds_attr': 'checked' if existing_data.get('exam_degree_stpm_uec') else '',
        'edm_attr': 'checked' if existing_data.get('exam_degree_matriculation') else '',
        'gspm_attr': 'checked' if existing_data.get('grade_spm') else '',
        'gstpm_attr': 'checked' if existing_data.get('grade_stpm') else '',
        'guec_attr': 'checked' if existing_data.get('grade_uec') else '',
        'gf_attr': 'checked' if existing_data.get('grade_foundation') else '',
        'dv_attr': 'checked' if existing_data.get('documents_verified') else '',
        'ab_attr': 'checked' if existing_data.get('academic_borderline') else '',
        'ac_attr': 'checked' if existing_data.get('academic_competent') else '',
        'as_attr': 'checked' if existing_data.get('academic_superior') else '',
        'ae_attr': 'checked' if existing_data.get('academic_elite') else '',
        'rbs_attr': 'checked' if existing_data.get('rigor_best_student') else '',
        'rc_attr': 'checked' if existing_data.get('rigor_competitions') else '',
        'rn_attr': 'checked' if existing_data.get('rigor_none') else '',
        'll_attr': 'checked' if existing_data.get('leadership_leader') else '',
        'ls_attr': 'checked' if existing_data.get('leadership_subleader') else '',
        'lsec_attr': 'checked' if existing_data.get('leadership_secretary') else '',
        'lcom_attr': 'checked' if existing_data.get('leadership_committee') else '',
        'lm_attr': 'checked' if existing_data.get('leadership_member') else '',
        'cn_attr': 'checked' if existing_data.get('competition_national') else '',
        'cs_attr': 'checked' if existing_data.get('competition_state') else '',
        'cu_attr': 'checked' if existing_data.get('competition_university') else '',
        'cp_attr': 'checked' if existing_data.get('competition_participant') else '',
    }
    return render(request, "reviewer/reviewScholarship.html", context)


def review_step2(request, app_id):
    app = ScholarshipApplication.objects.get(id=app_id)
    data = request.session.get(f'review_{app.id}', {})
    
    if request.method == "POST":
        fields = [
            'integrity_income_check', 'hardship_single_income', 'hardship_large_family',
            'hardship_retiree', 'hardship_medical', 'essay_compelling', 'essay_generic', 'essay_poor'
        ]
        for f in fields:
            data[f] = request.POST.get(f) == 'on'
        
        data['financial_priority'] = request.POST.get('financial_priority')
        
        request.session[f'review_{app.id}'] = data
        messages.success(request, "Step 2 progress cached.")
        
        if 'previous' in request.POST:
            return redirect('reviewer_with_id', app_id=app.id)
        return redirect('review_step3', app_id=app.id)

    guardians = app.guardians.all()
    total_income = sum(g.monthly_income for g in guardians)
    family_members = guardians.count() + 1
    pci = total_income / family_members if family_members > 0 else 0

    context = {
        'app': app,
        'data': data,
        'total_income_str': f"{total_income:,.2f}",
        'family_count': family_members,
        'pci_str': f"{pci:,.2f}",
        'integrity_attr': 'checked' if data.get('integrity_income_check') else '',
        'fp_1_attr': 'checked' if data.get('financial_priority') == '1' else '',
        'fp_2_attr': 'checked' if data.get('financial_priority') == '2' else '',
        'fp_3_attr': 'checked' if data.get('financial_priority') == '3' else '',
        'fp_4_attr': 'checked' if data.get('financial_priority') == '4' else '',
        'hs_attr': 'checked' if data.get('hardship_single_income') else '',
        'hl_attr': 'checked' if data.get('hardship_large_family') else '',
        'hr_attr': 'checked' if data.get('hardship_retiree') else '',
        'hm_attr': 'checked' if data.get('hardship_medical') else '',
        'ec_attr': 'checked' if data.get('essay_compelling') else '',
        'eg_attr': 'checked' if data.get('essay_generic') else '',
        'ep_attr': 'checked' if data.get('essay_poor') else '',
    }
    return render(request, "reviewer/review_step2.html", context)


def review_step3(request, app_id):
    app = ScholarshipApplication.objects.get(id=app_id)
    data = request.session.get(f'review_{app.id}', {})
    
    score = 0
    eligibility_checked = (
        data.get('citizenship_check') and 
        data.get('programme_level_check') and 
        (data.get('exam_foundation_spm') or data.get('exam_degree_stpm_uec') or data.get('exam_degree_matriculation')) and
        (data.get('grade_spm') or data.get('grade_stpm') or data.get('grade_uec') or data.get('grade_foundation')) and
        data.get('documents_verified')
    )
    if eligibility_checked:
        score += 5

    if data.get('integrity_income_check'):
        score += 5

    if data.get('academic_elite'):
        score += 30
    elif data.get('academic_superior'):
        score += 22
    elif data.get('academic_competent'):
        score += 15
    elif data.get('academic_borderline'):
        score += 8
    
    if data.get('rigor_best_student'):
        score += 5
    if data.get('rigor_competitions'):
        score += 5
    
    leadership_score = 0
    if data.get('leadership_leader'):
        leadership_score += 12
    elif data.get('leadership_subleader'):
        leadership_score += 9
    elif data.get('leadership_secretary'):
        leadership_score += 7
    elif data.get('leadership_committee'):
        leadership_score += 5
    elif data.get('leadership_member'):
        leadership_score += 2
    
    if data.get('competition_national'):
        leadership_score += 8
    elif data.get('competition_state'):
        leadership_score += 6
    elif data.get('competition_university'):
        leadership_score += 4
    elif data.get('competition_participant'):
        leadership_score += 2
    
    score += min(leadership_score, 20)
    
    financial_score = 0
    fp = data.get('financial_priority')
    if fp == '4':
        financial_score += 15
    elif fp == '3':
        financial_score += 11
    elif fp == '2':
        financial_score += 7
    elif fp == '1':
        financial_score += 3
    
    hardship_indicator = (
        data.get('hardship_single_income') or 
        data.get('hardship_large_family') or 
        data.get('hardship_retiree') or 
        data.get('hardship_medical')
    )
    if hardship_indicator:
        financial_score += 5
    
    score += min(financial_score, 20)
    
    if data.get('essay_compelling'):
        score += 10
    elif data.get('essay_generic'):
        score += 5
    
    total_score = int(score)

    if request.method == "POST":
        comment = request.POST.get('reviewer_comment', '')
        data['reviewer_comment'] = comment
        request.session[f'review_{app.id}'] = data

        if 'previous' in request.POST:
            return redirect('review_step2', app_id=app.id)

        if 'save' in request.POST or 'approve' in request.POST or 'reject' in request.POST:
            print(f"DEBUG: Processing form submission. POST keys: {request.POST.keys()}")
            
            ec, _ = EligibilityCheck.objects.get_or_create(application=app)
            for key, val in data.items():
                if hasattr(ec, key):
                    setattr(ec, key, val)
            ec.total_marks = total_score
            ec.save()
            print("DEBUG: EligibilityCheck saved.")
            
            if 'approve' in request.POST:
                print("DEBUG: Approving application...")
                ScholarshipApplication.objects.filter(id=app.id).update(status='Approved')
                # app.status = "Approved"
                # app.save()
                print(f"DEBUG: Application approved via update().")
                messages.success(request, f"Application for {app.name} has been APPROVED and saved.")
                return redirect('reviewer')
            elif 'reject' in request.POST:
                ScholarshipApplication.objects.filter(id=app.id).update(status='Rejected')
                # app.status = "Rejected"
                # app.save()
                messages.error(request, f"Application for {app.name} has been REJECTED.")
                return redirect('reviewer')
            else:
                messages.success(request, "Progress permanently saved to database.")
                return redirect('review_step3', app_id=app.id)

    ec_db = EligibilityCheck.objects.filter(application=app).first()
    context = {
        'app': app,
        'eligibility': {'reviewer_comment': data.get('reviewer_comment', ec_db.reviewer_comment if ec_db else '')},
        'score': total_score,
    }
    return render(request, "reviewer/review_step3.html", context)


def details(request):
    return render(request, "reviewer/reviewScholarship.html", {})

def index(request):
    applications = ScholarshipApplication.objects.all().order_by('submitted_date')
    
    for app in applications:
        if app.status == 'Approved':
            app.dashboard_status = 'Approved'
            app.dashboard_class = 'approved'
        elif app.status == 'Rejected':
            app.dashboard_status = 'Rejected'
            app.dashboard_class = 'rejected'
        elif f'review_{app.id}' in request.session:
            app.dashboard_status = 'In Progress'
            app.dashboard_class = 'in-progress'
        else:
            app.dashboard_status = 'To Review'
            app.dashboard_class = 'to-review'
            
    return render(request, "reviewer/reviewer.html", {'applications': applications})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
 
    def get(self, request, format=None):
        scholarships = Scholarship.objects.annotate(
            app_count=Count('applications')
        )
        data = {
            "labels": [s.name for s in scholarships],
            "chartLabel": "Scholarship Application Volume",
            "chartdata": [s.app_count for s in scholarships],
        }
        return Response(data)