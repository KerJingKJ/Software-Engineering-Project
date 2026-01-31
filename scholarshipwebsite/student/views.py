from django.utils import timezone 
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Application, Student, Guardian, Bookmark
from committee.models import Scholarship, Interview
from .forms import ApplicationForm, GuardianForm
from datetime import date
# Create your views here.
from django.contrib.auth.decorators import login_required
# Create your views here.
# views.py

def index(request):
    return render(request, "student/student.html", {})

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
    print(progress_track)

    return render(request, "student/applicationStatus.html", {'application':application, 'progress_track':progress_track})

@login_required
def eligibility_check(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('home')

    # 1. Start with active scholarships
    scholarships = Scholarship.objects.filter(deadline__gte=timezone.now().date())

    # --- GET INPUTS (Use Form Data if available, otherwise use Student Profile) ---
    search_level = request.GET.get('study_level') or student.education_level
    search_gpa = request.GET.get('gpa')
    
    # Use profile GPA if form GPA is empty
    if not search_gpa and student.current_gpa:
        search_gpa = student.current_gpa

    # 2. Filter by Level
    if search_level:
        scholarships = scholarships.filter(education_level=search_level)

    # 3. Filter by GPA
    if search_gpa:
        scholarships = scholarships.filter(min_gpa__lte=search_gpa)

    # 4. Filter by Student Type (Always stick to student's actual type for safety)
    if student.student_type:
        scholarships = scholarships.filter(student_type=student.student_type)

    return render(request, 'student/eligibility.html', {
        'student': student,
        'eligible_scholarships': scholarships, 
        # Pass these back so the form stays filled after searching
        'search_level': search_level,
        'search_gpa': search_gpa
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
    return render(request, 'student/applicationDetails.html', {
        'application': application,
        'guardians': guardians
    })