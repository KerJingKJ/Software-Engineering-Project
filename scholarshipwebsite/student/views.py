from django.utils import timezone 
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Application, Student, Guardian, Bookmark
from committee.models import Scholarship
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
        student.notifications.filter(is_read=False).update(is_read=True)
    except Student.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', 'student'))

from django.utils import timezone

@login_required
def notification_list(request):
    # --- MOCK DATA (Frontend Only) ---
    notifications = [
        {
            'message': 'Congratulations! Your application for Merit Scholarship 2026 has been APPROVED.',
            'created_at': timezone.now(),
            'is_read': False
        },
        {
            'message': 'Update: Your application for Future Leaders Award was REJECTED.',
            'created_at': timezone.now(),
            'is_read': True
        },
        {
            'message': 'Welcome to the Scholarship Portal! Please complete your profile.',
            'created_at': timezone.now(),
            'is_read': True
        }
    ]

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

def application_form_status(request):
    return render(request, "student/applicationForm_status.html", {})

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

def application_form(request):
    # db query via scholarship fk, if application exists. If exists, redirect to edit, or prefill info?
    # redirecting would implying there's a whole separate form for these. 
    scholarships = Scholarship.objects.all()
    # application = Application.objects.filter(scholarship_id=id).first()
    
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
        # return render(request, "student/applicationForm_p3.html", {"form": form, "application":application})
    elif page == 4:
        return render(request, "student/applicationForm_p4.html", {"form": form, "application":application})
    elif page == 5:
        return redirect("trackApplication")
    else:
        print (f"u stupid {page}")
        return redirect("application_form")

def guardian_form(request, id=-1, page=-1):
    if page != 3:
        return redirect("edit_application_form")
    
    application = get_object_or_404(Application, pk=id)

    if request.method == "POST":
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
        if form1.is_valid() and form2.is_valid():
            # Save first guardian
            guardian1 = form1.save()
            
            # Save second guardian
            guardian2 = form2.save()
            
            # Link guardians to application
            application.guardian1 = guardian1
            application.guardian2 = guardian2
            application.save()
            
            return redirect('edit_application_form', id=application.id, page=page+1)

        else:
            # Display errors
            print("Form 1 Errors:", form1.errors)
            print("Form 2 Errors:", form2.errors)
    else:
        # GET request - initialize forms with existing guardians
        form1 = GuardianForm(
            prefix='guardian1', 
            instance=application.guardian1
        )
        form2 = GuardianForm(
            prefix='guardian2', 
            instance=application.guardian2
        )
    
    return render(request, "student/applicationForm_p2.html", {
        "form1": form1, 
        "form2": form2, 
        "application": application,
        "page": page
    })

# def edit_application_form_p2(request, id, page):
#     # application = Application.objects.filter(scholarship_id=id).first()
#     return render(request, "student/applicationForm_p2.html", {})

# def edit_application_form_p3(request, id, page):
#     return render(request, "student/applicationForm_p3.html", {})

# def edit_application_form_p4(request, id, page):
#     return render(request, "student/applicationForm_p4.html", {})


@login_required
def trackApplication(request):
    # --- MOCK DATA (Frontend Only) ---
    # We create a fake list of applications to test the UI.
    applications = [
        {
            'id': 1,
            'scholarship': {'name': 'Merit Scholarship 2026'}, # Nested dict to mimic app.scholarship.name
            'submitted_date': date(2026, 1, 15),
            'status': 'Pending',
            'committee_status': 'Pending',
        },
        {
            'id': 2,
            'scholarship': {'name': 'Future Leaders Award'},
            'submitted_date': date(2025, 12, 10),
            'status': 'Rejected',
            'committee_status': 'Rejected',
        },
        {
            'id': 3,
            'scholarship': {'name': 'MMU Foundation Aid'},
            'submitted_date': date(2025, 11, 5),
            'status': 'Approved',
            'committee_status': 'Approved',
        }
    ]

    return render(request, "student/trackApplication.html", {
        'applications': applications
    })

@login_required
def application_detail(request, application_id):
    # --- MOCK DATA FOR A SINGLE APPLICATION ---
    # This simulates what a real application object would look like
    application = {
        'id': application_id,
        'scholarship': {'name': 'Merit Scholarship 2026'},
        'submitted_date': date(2026, 1, 15),
        'status': 'Pending',
        'committee_status': 'Pending',
        'name': 'Ali Bin Abu',
        'ic_no': '010101-10-1234',
        'email_address': 'ali@student.mmu.edu.my',
        'contact_number': '012-3456789',
        'date_of_birth': date(2003, 5, 20),
        'age': 23,
        'gender': 'Male',
        'nationality': 'Malaysian',
        'race': 'Malay',
        'home_address': '123 Jalan Multimedia, Cyberjaya',
        'correspondence_address': '123 Jalan Multimedia, Cyberjaya',
        'programme': 'Bachelor of Computer Science',
        'intake': date(2023, 3, 1),
        'education_level': 'Undergraduate',
        'monthly_income': '3500.00',
        'reason_deserve': 'I have maintained a 4.0 GPA while volunteering...',
        'personal_achievement': 'Dean List 2024, Hackathon Winner',
    }

    # Mock Guardians
    guardians = [
        {
            'name': 'Abu Bakar',
            'relationship': 'Father',
            'contact_number': '019-8765432',
            'email_address': 'abu@email.com'
        }
    ]

    return render(request, 'student/application_detail.html', {
        'application': application,
        'guardians': guardians
    })
# Create your views here.
