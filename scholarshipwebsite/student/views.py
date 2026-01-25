from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Student, Bookmark
from committee.models import Scholarship
from .models import Application
from .forms import ApplicationForm
# Create your views here.
# views.py

def index(response):
    return render(response, "student/student.html", {})

def scholarship_list(request):
    # Fetch all scholarships from the database
    scholarships = Scholarship.objects.all()
    
    # Pass them to the template
    return render(request, "student/scholarshipList.html", {
        'scholarships': scholarships
    })

def scholarship_details(response):
    return render(response, "student/scholarshipDetails.html", {})

@login_required
def eligibility_check(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('home')

    # Start with all active scholarships
    # Adjust 'status' field if your model uses a different name
    eligible_scholarships = Scholarship.objects.filter(status='Active')

    # --- FILTER LOGIC ---
    # 1. Filter by Education Level (e.g., Undergraduate, Foundation)
    if student.education_level:
        eligible_scholarships = eligible_scholarships.filter(
            education_level__icontains=student.education_level
        )

    # 2. Filter by GPA (Scholarship min_gpa <= Student current_gpa)
    # Check if your Scholarship model has a 'min_gpa' or 'minimum_gpa' field
    if student.current_gpa:
        eligible_scholarships = eligible_scholarships.filter(
            min_gpa__lte=student.current_gpa
        )

    # 3. Filter by Student Type (Local/International)
    if student.student_type:
        eligible_scholarships = eligible_scholarships.filter(
            student_type__iexact=student.student_type
        )

    context = {
        'student': student,
        'eligible_scholarships': eligible_scholarships,
    }
    return render(request, 'student/eligibility.html', context)

def application_form(response):
    return render(response, "student/applicationForm.html", {})

def application_form_p2(response):
    return render(response, "student/applicationForm_p2.html", {})

def application_form_p3(response):
    return render(response, "student/applicationForm_p3.html", {})

def application_form_p4(response):
    return render(response, "student/applicationForm_p4.html", {})

def application_form_status(response):
    return render(response, "student/applicationForm_status.html", {})

def track(response):
    return render(response, "student/trackApplication.html", {})

@login_required
def toggle_bookmark(request, scholarship_id):
    """
    Adds or removes a scholarship from the student's bookmarks.
    """
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
def scholarship_details(request, scholarship_id):
    """
    Displays details and checks if the scholarship is bookmarked.
    """
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
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
    """
    Displays the list of bookmarked scholarships.
    """
    try:
        student = request.user.student
        # Get the list of bookmark objects
        my_bookmarks = Bookmark.objects.filter(student=student).select_related('scholarship').order_by('-date_added')
    except Student.DoesNotExist:
        my_bookmarks = []

    return render(request, 'student/bookmarkScholarship.html', {
        'bookmarks': my_bookmarks
    })
# Create your views here.
