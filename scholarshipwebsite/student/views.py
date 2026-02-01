from django.utils import timezone 
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Application, Student, Guardian, Bookmark, Notification
from committee.models import Scholarship, Interview
from .forms import ApplicationForm, GuardianForm
from datetime import date
from django.contrib.auth.decorators import login_required
from committee.models import CommitteeNotification
# Create your views here.
# views.py

def index(request):
    latest_app = None
    scholarship_status = "No Application" 
    recommended_scholarships = []

    if request.user.is_authenticated and hasattr(request.user, 'student'):
        student = request.user.student
        # Get the most recent application
        latest_app = Application.objects.filter(student=student).order_by('-submitted_date').first()
        
        if latest_app:
            # Determine status (reusing the logic from the previous step)
            if latest_app.reviewer_status == "Rejected" or latest_app.committee_status == "Rejected":
                scholarship_status = "Rejected"
            elif latest_app.committee_status == "Approved":
                scholarship_status = "Approved"
            else:
                scholarship_status = "Pending"

        active_scholarships = Scholarship.objects.filter(deadline__gte=timezone.now().date())
        
        # Filter by CGPA (Scholarship Min GPA <= Student Current GPA)
        if student.current_gpa:
            active_scholarships = active_scholarships.filter(min_gpa__lte=student.current_gpa)
            
        # Optional: Filter by Education Level & Student Type for better accuracy
        if student.education_level:
            active_scholarships = active_scholarships.filter(education_level=student.education_level)
        if student.student_type:
            active_scholarships = active_scholarships.filter(student_type=student.student_type)
            
        # Take the first 3 matching scholarships
        recommended_scholarships = active_scholarships.order_by('deadline')[:3]

    return render(request, "student/student.html", {
        'latest_app': latest_app,
        'scholarship_status': scholarship_status,
        'recommended_scholarships': recommended_scholarships  # Pass this to template
    })

@login_required
def mark_all_read(request):
    try:
        student = request.user.student
        student.notifications.filter(is_read=False, display_at__lte=timezone.now()).update(is_read=True)
    except Student.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', 'student'))

from django.utils import timezone

@login_required
def notification_list(request):
    notifications = (request.user.student.notifications.filter(display_at__lte=timezone.now()))

    return render(request, 'student/notifications.html', {
        'notifications': notifications
    })
    
def scholarship_list(request):
    # Fetch all scholarships from the database
    scholarships = Scholarship.objects.all()
    
    # Pass them to the template
    return render(request, "student/scholarshipList.html", {
        'scholarships': scholarships
    })

def applicationStatus(request, id):
    application = get_object_or_404(Application, pk=id)

    # progress_track = ""
    # if application.iscomplete:
    #     progress_track = "Pending"
    if application.reviewer_status== "Rejected" or application.committee_status== "Rejected":
        progress_track = "Rejected"
    elif application.committee_status== "Approved":
        progress_track = "Approved"
    elif application.reviewer_status == "Pending":
        progress_track = "Under Review"
    elif application.reviewer_status == "Reviewed" and application.committee_status == "Pending":
        if application.interviews.exists():
            progress_track = "Interview"
        else:
            progress_track = "Reviewed"

    return render(request, "student/applicationStatus.html", {'application':application, 'progress_track':progress_track})
def eligibility_check(request):
    # 1. Capture GET inputs (Profile is now optional)
    search_qual = request.GET.get('qualification')
    search_level = request.GET.get('study_level')
    search_gpa = request.GET.get('gpa')
    search_as = request.GET.get('a_count')

    # 2. Initial Filter (Active & Level)
    scholarships = Scholarship.objects.filter(deadline__gte=timezone.now().date())
    
    if search_level:
        scholarships = scholarships.filter(education_level=search_level)

    eligible_scholarships = []

    # 3. Match logic
    for scholarship in scholarships:
        criteria_list = scholarship.criteria_list.all()
        
        # If no criteria exist, it's open to all in that study level
        if not criteria_list:
            eligible_scholarships.append(scholarship)
            continue

        match_found = False
        for criteria in criteria_list:
            # First, qualification MUST match
            if search_qual and criteria.qualification == search_qual:
                
                # Logic for 'GPA' type
                if criteria.criteria_type == 'GPA' and search_gpa:
                    if float(search_gpa) >= float(criteria.min_value):
                        match_found = True
                
                # Logic for 'A_COUNT' type (e.g., SPM 9As)
                elif criteria.criteria_type == 'A_COUNT' and search_as:
                    if int(search_as) >= int(criteria.min_value):
                        match_found = True
                
                # Logic for 'TEXT' (Always show so they can read manual reqs)
                elif criteria.criteria_type == 'TEXT':
                    match_found = True

            if match_found:
                eligible_scholarships.append(scholarship)
                break

    return render(request, 'student/eligibility.html', {
        'eligible_scholarships': eligible_scholarships,
        'search_level': search_level,
        'search_gpa': search_gpa,
        'search_qual': search_qual,
        'search_as': search_as,
    })

@login_required
def toggle_bookmark(request, scholarship_id):
    # Get the logged-in student (handle case where admin/user has no student profile)
    if not hasattr(request.user, 'student'):
        messages.error(request, "Only students can bookmark scholarships.")
        return redirect('scholarship_list') # Redirect non-students safely
    student = request.user.student
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)

    # Check if it's already bookmarked
    bookmark = Bookmark.objects.filter(student=student, scholarship=scholarship).first()
    
    if bookmark:
        bookmark.delete() # Remove if exists
        messages.success(request, "Scholarship removed from bookmarks.")
    else:
        Bookmark.objects.create(student=student, scholarship=scholarship) # Add if not exists
        messages.success(request, "Scholarship added to bookmarks.")
    
    # Redirect back to the page the user came from
    return redirect(request.META.get('HTTP_REFERER', 'scholarship_list'))


@login_required
def scholarship_details(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    is_bookmarked = False

    # Check if user is a student and has bookmarked this
    if hasattr(request.user, 'student'):
        is_bookmarked = Bookmark.objects.filter(
            student=request.user.student, 
            scholarship=scholarship
        ).exists()

    return render(request, 'student/scholarshipDetails.html', {
        'scholarship': scholarship,
        'is_bookmarked': is_bookmarked
    })


@login_required
def bookmark_list(request):
    try:
        student = request.user.student
        # Get the list of bookmark objects
        my_bookmarks = Bookmark.objects.filter(student=student).select_related('scholarship').order_by('-date_added')
    except Student.DoesNotExist:
        my_bookmarks = []

    return render(request, 'student/bookmarkScholarship.html', {
        'bookmarks': my_bookmarks
    })

def application_form(request):
    scholarships = Scholarship.objects.all()

    
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)


        if form.is_valid():

            application = form.save(commit=False)
            try:
                application.student = request.user.student
            except Student.DoesNotExist:
                form.add_error(None, "Not a student.")
                print(form.errors)
                return render(
                    request,
                    "student/applicationForm.html",
                    {"form": form, "scholarships": scholarships},
                )
            application.save()
            return redirect("edit_application_form", id=application.pk, page=2)
        else:
            print(form.errors)
    else:
        form = ApplicationForm()
    return render(request, "student/applicationForm.html", {"form":form, "scholarships":scholarships})

def edit_application_form(request, id=-1, page=-1):
    application = get_object_or_404(Application, pk=id)
    scholarships = Scholarship.objects.all()
    scholarship = application.scholarship
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        # special handling of internal guardian forms 
        if page==3:
            form1 = GuardianForm(
                request.POST, 
                request.FILES, 
                prefix='guardian1',
                instance=application.guardian1  # None or existing Guardian
            )
            form2 = GuardianForm(
                request.POST, 
                request.FILES, 
                prefix='guardian2',
                instance=application.guardian2  # None or existing Guardian
            )
            
            # Validate both forms
            if form1.is_valid():
                # Save first guardian
                guardian1 = form1.save()
                application.guardian1 = guardian1

            if form2.is_valid():
                # Save second guardian
                guardian2 = form2.save()
                application.guardian2 = guardian2
            application.save()
        if form.is_valid():
            form.save()
            return redirect("edit_application_form", id=id, page=(page+1))
        else:
            print(form.errors)
    else:
        form = ApplicationForm(instance=application)

    if page == 1:
        return render(request, "student/applicationForm.html", {"form": form, "application":application, "scholarships":scholarships})
    elif page == 2:
        return render(request, "student/applicationForm_p2.html", {"form": form, "application":application})
    elif page == 3:
# GET request - initialize forms with existing guardians
        form1 = GuardianForm(
            prefix='guardian1', 
            instance=application.guardian1
        )
        form2 = GuardianForm(
            prefix='guardian2', 
            instance=application.guardian2
        )
        return render(request, "student/applicationForm_p3.html", {
            "form": form,
            "application": application,
            "page": page,
            "form1": form1, 
            "form2": form2, 
            "application": application,

        })
    elif page == 4:
        return render(request, "student/applicationForm_p4.html", {"form": form, "application":application})
    elif page == 5:
        return redirect("applicationStatus", id=id)
    else:
        print (f"u stupid {page}")
        return redirect("application_form")

@login_required
def applications(request):
    applications = request.user.student.applications.all()
    return render(request, "student/applications.html", {
        'applications': applications
    })

@login_required
def application_detail(request, id):
    application = get_object_or_404(Application, pk=id)
    guardians = [application.guardian1, application.guardian2]
    interview = (
        Interview.objects
        .filter(application=application)
        .order_by('-updated_at')
        .first())

    progress_track = "Pending"
    if application.reviewer_status== "Rejected" or application.committee_status== "Rejected":
        progress_track = "Rejected"
    elif application.committee_status== "Approved":
        progress_track = "Approved"
    elif application.reviewer_status == "Pending":
        progress_track = "Under Review"
    elif application.reviewer_status == "Reviewed" and application.committee_status == "Pending":
        if interview:
            progress_track = "Interview"
        else:
            progress_track = "Reviewed"

    return render(request, 'student/applicationDetails.html', {
        'application': application,
        'guardians': guardians,
        'interview':interview,
        'progress_track':progress_track
    })


# In scholarshipwebsite/student/views.py

def reschedule_interview(request, id):
    application = get_object_or_404(Application, pk=id)
    # Get the specific interview linked to this application
    interview = get_object_or_404(Interview, application=application)
    
    if request.method == "POST":
        date = request.POST.get('date')
        interview_time = request.POST.get('interview_time')
        timezone = request.POST.get('timezone')

        # 1. Check for conflicts
        conflict = Interview.objects.filter(date=date, interview_time=interview_time).exclude(application=application).exists()
        
        if conflict:
            messages.error(request, f"The time slot {interview_time} on {date} is already taken. Please choose another time.")
            return redirect('application_detail', id=id)

        # 2. Update the interview details
        interview.date = date
        interview.interview_time = interview_time
        interview.timezone = timezone
        interview.save() # Save the changes

        # 3. Notify the Committee (ONE TIME ONLY)
        # We check who should be notified: either the assigned member OR the person who created the interview
        recipient = application.assigned_committee_member or interview.committee

        if recipient:
            CommitteeNotification.objects.create(
                user=recipient,
                message=(
                    f"Reschedule Alert: {application.name} "
                    f"changed their interview for {application.scholarship.name} "
                    f"to {interview.date} at {interview.interview_time}."
                )
            )
        
        # 4. Notify the Student (ONE TIME ONLY)
        Notification.objects.create(
            student=application.student,
            type="System",
            message=f"Reschedule Confirmed: You have successfully rescheduled your interview for {application.scholarship.name} to {date} at {interview_time}."
        )
        
        return redirect('application_detail', id=id)

    return render(request, "student/reschedule_interview.html", {
        'application': application,
        'existing_interview': interview,
        'is_scheduled': interview is not None
    })
