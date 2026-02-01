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
        if student.education_level:
            active_scholarships = active_scholarships.filter(education_level=student.education_level)
        if student.student_type:
            active_scholarships = active_scholarships.filter(student_type=student.student_type)
            
        # Optional: Filter by Education Level & Student Type for better accuracy
        if student.current_gpa:
            # Optimize by prefetching criteria to avoid database spam
            scholarship_list = list(active_scholarships.prefetch_related('criteria_list'))
            filtered_list = []

            for scholarship in scholarship_list:
                # Find if there is a GPA requirement
                gpa_criteria = None
                for criteria in scholarship.criteria_list.all():
                    if criteria.criteria_type == 'GPA':
                        gpa_criteria = criteria
                        break
                
                # Logic: If GPA criteria exists, check against student's GPA. 
                # If NO GPA criteria exists, assume it's open/eligible.
                if gpa_criteria and gpa_criteria.min_value:
                    if student.current_gpa >= float(gpa_criteria.min_value):
                        filtered_list.append(scholarship)
                else:
                    filtered_list.append(scholarship)
            
            # Use the filtered list
            active_scholarships = filtered_list
            
        if isinstance(active_scholarships, list):
            # Sort list by deadline
            active_scholarships.sort(key=lambda x: x.deadline)
            recommended_scholarships = active_scholarships[:3]
        else:
            # Sort QuerySet by deadline
            recommended_scholarships = active_scholarships.order_by('deadline')[:3]
            
        # Take the first 3 matching scholarships

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

@login_required
def respond_to_offer(request, id, response):
    # Fetch the application and ensure it belongs to the logged-in student
    application = get_object_or_404(Application, pk=id, student=request.user.student)
    
    # Security check: only allow response if committee has approved
    if application.committee_status != 'Approved':
        messages.error(request, "You cannot respond to an application that is not yet approved.")
        return redirect('application_detail', id=id)
    
    # Update status based on student's choice
    if response in ['Accepted', 'Declined']:
        application.acceptance_status = response
        application.save()
        
        status_msg = "accepted" if response == "Accepted" else "declined"
        messages.success(request, f"You have successfully {status_msg} the scholarship offer.")
    
    return redirect('application_detail', id=id)

def eligibility_check(request):
    try:
        student = request.user.student
    except AttributeError:
        # Handle case where user is admin/committee or not logged in
        student = None

    # 1. Fetch Active Scholarships
    scholarships = Scholarship.objects.filter(
        deadline__gte=timezone.now().date()
    ).prefetch_related('criteria_list')

    # 2. Get Inputs (from GET request or Student Profile)
    # Default to profile data if inputs are empty
    search_qual = request.GET.get('qualification')
    search_gpa = request.GET.get('gpa')
    search_as = request.GET.get('a_count')

    if student:
        if not search_qual:
            search_qual = student.qualification # e.g. "Foundation"
        if not search_gpa and student.current_gpa:
            search_gpa = student.current_gpa
        if not search_as and student.a_count:
            search_as = student.a_count

    eligible_scholarships = []

    # 3. Matching Logic
    if search_qual: 
        # Convert inputs to float for comparison (handle empty strings)
        try:
            user_gpa = float(search_gpa) if search_gpa else 0.0
            user_as = int(search_as) if search_as else 0
        except ValueError:
            user_gpa = 0.0
            user_as = 0

        for scholarship in scholarships:
            is_match = False
            # Check every criteria set by the committee
            for criteria in scholarship.criteria_list.all():
                
                # A. Check Qualification Match (e.g. "SPM" == "SPM")
                if criteria.qualification.strip().lower() == search_qual.strip().lower():
                    
                    # B. Check Requirement based on Type
                    if criteria.criteria_type == 'GPA':
                        # Compare GPA
                        if criteria.min_value and user_gpa >= criteria.min_value:
                            is_match = True
                            # Pass entitlement data to the template for this specific match
                            scholarship.matching_entitlement = criteria.entitlement 
                    
                    elif criteria.criteria_type == 'A_COUNT':
                        # Compare Number of As
                        if criteria.min_value and user_as >= criteria.min_value:
                            is_match = True
                            scholarship.matching_entitlement = criteria.entitlement

                    elif criteria.criteria_type == 'TEXT':
                        # Always show text-based criteria (manual review needed)
                        is_match = True
                        scholarship.matching_entitlement = criteria.entitlement

                if is_match:
                    eligible_scholarships.append(scholarship)
                    break # Stop checking other criteria for this scholarship if one matches

    else:
        # If no search performed, show all active (or none, depending on preference)
        eligible_scholarships = scholarships

    return render(request, 'student/eligibility.html', {
        'student': student,
        'eligible_scholarships': eligible_scholarships,
        'search_qual': search_qual,
        'search_gpa': search_gpa,
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
