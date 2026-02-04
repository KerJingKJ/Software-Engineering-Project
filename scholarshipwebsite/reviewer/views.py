from django.shortcuts import render, redirect
from django.db.models import Count, F
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.db import models
from committee.models import Scholarship
from student.models import Student, Application
from .models import EligibilityCheck

@login_required
def index(request):
    """
    Renders the main dashboard page.
    """
    # Calculate summary stats for cards
 
    user_apps = Application.objects.filter(assigned_reviewer=request.user)
    total_apps = user_apps.count()
    committee_rejected = user_apps.filter(committee_status='Rejected').count() 
    reviewer_rejected =  user_apps.filter(reviewer_status='Rejected').count()
    rejected = committee_rejected + reviewer_rejected
    committee_pending = user_apps.filter(committee_status='Pending').count() 
    pending = committee_pending - reviewer_rejected
    
    context = {
        'total_apps': total_apps,
        'rejected': rejected,
        'pending': pending
    }
    return render(request, "reviewer/reviewer.html", context)

@login_required
def review_list(request):
    applications = Application.objects.filter(assigned_reviewer = request.user).order_by('submitted_date')
    
    for app in applications:
        # Determine display status based on session or DB
        if app.reviewer_status == 'Reviewed': #reviewed
            app.dashboard_status = 'Reviewed'
            app.dashboard_class = 'reviewed'
        elif app.reviewer_status == 'Rejected': #rejected
            app.dashboard_status = 'Rejected'
            app.dashboard_class = 'rejected'
        elif f'review_{app.id}' in request.session:
            app.dashboard_status = 'In Progress'
            app.dashboard_class = 'in-progress'
        else: #pending
            app.dashboard_status = 'To Review'
            app.dashboard_class = 'to-review'
            
    return render(request, "reviewer/review_list.html", {'applications': applications})

@login_required
def review_detail(request, app_id):
    app = Application.objects.filter(id=app_id).first()
    if not app:
        return redirect('review')

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
        request.session.modified = True  # Ensure session is saved
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
        # Eligibility checks
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
        # Academic scoring
        'ab_attr': 'checked' if existing_data.get('academic_borderline') else '',
        'ac_attr': 'checked' if existing_data.get('academic_competent') else '',
        'as_attr': 'checked' if existing_data.get('academic_superior') else '',
        'ae_attr': 'checked' if existing_data.get('academic_elite') else '',
        # Rigor
        'rbs_attr': 'checked' if existing_data.get('rigor_best_student') else '',
        'rc_attr': 'checked' if existing_data.get('rigor_competitions') else '',
        'rn_attr': 'checked' if existing_data.get('rigor_none') else '',
        # Leadership
        'll_attr': 'checked' if existing_data.get('leadership_leader') else '',
        'ls_attr': 'checked' if existing_data.get('leadership_subleader') else '',
        'lsec_attr': 'checked' if existing_data.get('leadership_secretary') else '',
        'lcom_attr': 'checked' if existing_data.get('leadership_committee') else '',
        'lm_attr': 'checked' if existing_data.get('leadership_member') else '',
        # Competition
        'cn_attr': 'checked' if existing_data.get('competition_national') else '',
        'cs_attr': 'checked' if existing_data.get('competition_state') else '',
        'cu_attr': 'checked' if existing_data.get('competition_university') else '',
        'cp_attr': 'checked' if existing_data.get('competition_participant') else '',
    }
    return render(request, "reviewer/reviewScholarship.html", context)

@login_required
def review_step2(request, app_id):
    app = Application.objects.filter(id=app_id).first()
    if not app:
        return redirect('review')
    
    # Step 2 fields - now hardship and essay are single radio values
    if request.method == "POST":
        # Get existing session data (from step 1)
        data = request.session.get(f'review_{app.id}', {})
        
        # Save step 2 fields
        data['integrity_income_check'] = request.POST.get('integrity_income_check') == 'on'
        data['financial_priority'] = request.POST.get('financial_priority', '')
        
        # Hardship - radio button, convert to individual booleans for DB compatibility
        hardship_value = request.POST.get('hardship', '')
        data['hardship_single_income'] = hardship_value == 'single_income'
        data['hardship_large_family'] = hardship_value == 'large_family'
        data['hardship_retiree'] = hardship_value == 'retiree'
        data['hardship_medical'] = hardship_value == 'medical'
        data['hardship'] = hardship_value  # Store the actual value too
        
        # Essay - radio button, convert to individual booleans for DB compatibility
        essay_value = request.POST.get('essay', '')
        data['essay_compelling'] = essay_value == 'compelling'
        data['essay_generic'] = essay_value == 'generic'
        data['essay_poor'] = essay_value == 'poor'
        data['essay'] = essay_value  # Store the actual value too
        
        # Save to session
        request.session[f'review_{app.id}'] = data
        request.session.modified = True  # Ensure session is saved
        
        # Handle navigation
        if 'previous' in request.POST:
            return redirect('reviewer_with_id', app_id=app.id)
        elif 'next' in request.POST:
            return redirect('review_step3', app_id=app.id)
    
    # Load existing data from session or DB
    # First check if we have step 2 data in session, otherwise load from DB
    session_data = request.session.get(f'review_{app.id}', {})
    
    # Check if step 2 fields exist in session
    has_step2_in_session = 'hardship' in session_data or 'essay' in session_data or 'financial_priority' in session_data
    
    # Load from database
    ec = EligibilityCheck.objects.filter(application=app).first()
    
    if ec and not has_step2_in_session:
        # Load step 2 data from database
        existing_data = session_data.copy()  # Keep step 1 data if exists
        existing_data.update({
            'integrity_income_check': ec.integrity_income_check,
            'financial_priority': ec.financial_priority or '',
            'hardship_single_income': ec.hardship_single_income,
            'hardship_large_family': ec.hardship_large_family,
            'hardship_retiree': ec.hardship_retiree,
            'hardship_medical': ec.hardship_medical,
            'essay_compelling': ec.essay_compelling,
            'essay_generic': ec.essay_generic,
            'essay_poor': ec.essay_poor,
        })
        # Derive radio values from booleans
        if ec.hardship_single_income: existing_data['hardship'] = 'single_income'
        elif ec.hardship_large_family: existing_data['hardship'] = 'large_family'
        elif ec.hardship_retiree: existing_data['hardship'] = 'retiree'
        elif ec.hardship_medical: existing_data['hardship'] = 'medical'
        else: existing_data['hardship'] = ''
        
        if ec.essay_compelling: existing_data['essay'] = 'compelling'
        elif ec.essay_generic: existing_data['essay'] = 'generic'
        elif ec.essay_poor: existing_data['essay'] = 'poor'
        else: existing_data['essay'] = ''
    else:
        existing_data = session_data
    
    # Get guardians for display
    guardians = []
    if app.guardian1:
        guardians.append(app.guardian1)
    if app.guardian2:
        guardians.append(app.guardian2)
    
    # Calculate PCI (Per Capita Income)
    total_income = float(app.monthly_income) if app.monthly_income else 0
    family_count = 1 + len(guardians)  # Student + guardians
    pci = total_income / family_count if family_count > 0 else 0
    
    # Prepare checked attributes for template
    fp_value = existing_data.get('financial_priority', '')
    hardship_value = existing_data.get('hardship', '')
    essay_value = existing_data.get('essay', '')
    
    context = {
        'app': app,
        'guardians': guardians,
        'data': existing_data,
        'total_income_str': f"{total_income:,.2f}",
        'family_count': family_count,
        'pci_str': f"{pci:,.2f}",
        # Checked attributes
        'integrity_attr': 'checked' if existing_data.get('integrity_income_check') else '',
        'fp_1_attr': 'checked' if fp_value == '1' else '',
        'fp_2_attr': 'checked' if fp_value == '2' else '',
        'fp_3_attr': 'checked' if fp_value == '3' else '',
        'fp_4_attr': 'checked' if fp_value == '4' else '',
        # Hardship radio
        'hs_attr': 'checked' if hardship_value == 'single_income' else '',
        'hl_attr': 'checked' if hardship_value == 'large_family' else '',
        'hr_attr': 'checked' if hardship_value == 'retiree' else '',
        'hm_attr': 'checked' if hardship_value == 'medical' else '',
        # Essay radio
        'ec_attr': 'checked' if essay_value == 'compelling' else '',
        'eg_attr': 'checked' if essay_value == 'generic' else '',
        'ep_attr': 'checked' if essay_value == 'poor' else '',
    }
    return render(request, "reviewer/review_step2.html", context)

@login_required
def review_step3(request, app_id):
    app = Application.objects.filter(id=app_id).first()
    if not app:
        return redirect('review')
    
    # Get session data from step 1 and step 2
    session_data = request.session.get(f'review_{app.id}', {})
    
    # Calculate score based on the rubric (Total: 100 marks)
    score = 0
    
    # 1. Eligibility Checklist (5 marks) - All 5 boxes must be checked for +5, else 0
    eligibility_fields = ['citizenship_check', 'programme_level_check', 'exam_foundation_spm', 
                          'exam_degree_stpm_uec', 'exam_degree_matriculation']
    # Check if at least one exam type AND citizenship AND programme level are checked
    exam_checked = (session_data.get('exam_foundation_spm') or 
                   session_data.get('exam_degree_stpm_uec') or 
                   session_data.get('exam_degree_matriculation'))
    if (session_data.get('citizenship_check') and 
        session_data.get('programme_level_check') and 
        exam_checked and
        session_data.get('documents_verified')):
        score += 5
    
    # 2. Data Integrity Check (5 marks) - Income Proof Match box must be checked
    if session_data.get('integrity_income_check'):
        score += 5
    
    # 3. Academic Performance (30 marks max)
    if session_data.get('academic_elite'): score += 30
    elif session_data.get('academic_superior'): score += 22
    elif session_data.get('academic_competent'): score += 15
    elif session_data.get('academic_borderline'): score += 8
    
    # 4. Academic Rigor & Awards (10 marks max - 5 marks each)
    if session_data.get('rigor_best_student'): score += 5
    if session_data.get('rigor_competitions'): score += 5
    
    # 5. Leadership (20 marks max)
    # A. Highest Position Held (Max 12 Marks)
    if session_data.get('leadership_leader'): score += 12
    elif session_data.get('leadership_subleader'): score += 9
    elif session_data.get('leadership_secretary'): score += 7
    elif session_data.get('leadership_committee'): score += 5
    elif session_data.get('leadership_member'): score += 2
    
    # B. Competition/Event Achievement (Max 8 Marks)
    if session_data.get('competition_national'): score += 8
    elif session_data.get('competition_state'): score += 6
    elif session_data.get('competition_university'): score += 4
    elif session_data.get('competition_participant'): score += 2
    
    # 6. Financial/Hardship (20 marks max)
    # A. Financial Priority (max 15 marks)
    fp = session_data.get('financial_priority', '')
    if fp == '4': score += 15    # Critical Need (Below 1,200)
    elif fp == '3': score += 11  # High Need (1,201-2,500)
    elif fp == '2': score += 7   # Moderate Need (2,501-5,000)
    elif fp == '1': score += 3   # Low Need (Above 5,000)
    
    # B. Hardship (max 5 marks) - if any ticks, add 5
    has_hardship = (session_data.get('hardship_single_income') or 
                   session_data.get('hardship_large_family') or 
                   session_data.get('hardship_retiree') or 
                   session_data.get('hardship_medical'))
    if has_hardship:
        score += 5
    
    # 7. Personal Statement / Essay Quality (10 marks)
    if session_data.get('essay_compelling'): score += 10
    elif session_data.get('essay_generic'): score += 5
    elif session_data.get('essay_poor'): score += 0
    
    # Get or create EligibilityCheck
    eligibility, created = EligibilityCheck.objects.get_or_create(application=app)
    
    if request.method == "POST":
        # Handle Previous button
        if 'previous' in request.POST:
            return redirect('review_step2', app_id=app.id)
        
        # Save all data to database
        all_fields = [
            'citizenship_check', 'programme_level_check', 'exam_foundation_spm',
            'exam_degree_stpm_uec', 'exam_degree_matriculation', 'grade_spm',
            'grade_stpm', 'grade_uec', 'grade_foundation', 'documents_verified',
            'academic_borderline', 'academic_competent', 'academic_superior', 'academic_elite',
            'rigor_best_student', 'rigor_competitions', 'rigor_none',
            'leadership_leader', 'leadership_subleader', 'leadership_secretary',
            'leadership_committee', 'leadership_member', 'competition_national',
            'competition_state', 'competition_university', 'competition_participant',
            'integrity_income_check', 'hardship_single_income', 'hardship_large_family',
            'hardship_retiree', 'hardship_medical', 'essay_compelling', 'essay_generic', 'essay_poor'
        ]
        
        for field in all_fields:
            setattr(eligibility, field, session_data.get(field, False))
        
        eligibility.financial_priority = session_data.get('financial_priority', '')
        eligibility.total_marks = score
        eligibility.reviewer_comment = request.POST.get('reviewer_comment', '')
        eligibility.save()
        
        # Handle Save button
        if 'save' in request.POST:
            Application.objects.filter(id=app.id).update(reviewer_status='Reviewed')
            request.session.pop(f'review_{app.id}', None)

            from django.contrib import messages
            messages.success(request, 'Review saved successfully!')
            return redirect('review')
        
        # Handle Reject button
        if 'reject' in request.POST:
            Application.objects.filter(id=app.id).update(reviewer_status='Rejected')
            # Clear session data
            if f'review_{app.id}' in request.session:
                del request.session[f'review_{app.id}']
            return redirect('review')
    
    context = {
        'app': app,
        'score': score,
        'eligibility': eligibility,
    }
    return render(request, "reviewer/review_step3.html", context)
    
def details(request):
    return render(request, "reviewer/reviewScholarship.html", {})



class ChartData(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
 
    def get(self, request, format=None):
        # Filter applications by the logged-in reviewer
        user_apps_query = Application.objects.filter(assigned_reviewer=request.user)

        # 1. Growth Chart: Cumulative Applications
        daily_apps = user_apps_query.values('submitted_date').annotate(
            count=Count('id')
        ).order_by('submitted_date')
        
        line_labels = []
        line_data = []
        cumulative_count = 0
        for entry in daily_apps:
            if entry['submitted_date']:
                line_labels.append(entry['submitted_date'].strftime('%d-%m-%Y'))
                cumulative_count += entry['count']
                line_data.append(cumulative_count)

        # 2. Status Chart: Rejected vs Pending
        rejected = user_apps_query.filter(committee_status='Rejected').count()
        pending = user_apps_query.exclude(committee_status__in=['Approved', 'Rejected']).count()
        
        # 3. Popularity Chart: Apps per Scholarship (Only for assigned apps)
        scholarships = Scholarship.objects.filter(application__in=user_apps_query).annotate(
            count=Count('application', filter=models.Q(application__assigned_reviewer=request.user))
        ).distinct()
        sch_labels = [s.name for s in scholarships]
        sch_data = [s.count for s in scholarships]

        # 4. Demographic Chart: Education Level
        edu_levels = user_apps_query.values('student__education_level').annotate(
            count=Count('id')
        )
        edu_labels = [e['student__education_level'] for e in edu_levels if e['student__education_level']]
        edu_data = [e['count'] for e in edu_levels if e['student__education_level']]

        data = {
            "growth_chart": {
                "labels": line_labels,
                "data": line_data,
                "label": "Total Applications"
            },
            "status_chart": {
                "labels": ["Rejected", "Pending"],
                "data": [rejected, pending]
            },
            "scholarship_chart": {
                "labels": sch_labels,
                "data": sch_data,
                "label": "Applications"
            },
            "education_chart": {
                "labels": edu_labels,
                "data": edu_data
            }
        }
        return Response(data)
