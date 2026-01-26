from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Application, Student, Guardian
from committee.models import Scholarship
from .forms import ApplicationForm, GuardianForm
# Create your views here.
# views.py

def index(request):
    return render(request, "student/student.html", {})

def scholarship_list(request):
    return render(request, "student/scholarshipList.html", {})

def eligibility(request):
    return render(request, "student/eligibility.html", {})

def application_form_status(request):
    return render(request, "student/applicationForm_status.html", {})

def scholarship_details(request, id):
    return render(request, "student/scholarshipDetails.html", {})

def bookmark_scholarship(request, id):
    return render(request, "student/bookmarkScholarship.html", {})


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
            if form1.is_valid() and form2.is_valid():
                # Save first guardian
                guardian1 = form1.save()
                
                # Save second guardian
                guardian2 = form2.save()
                
                # Link guardians to application
                application.guardian1 = guardian1
                application.guardian2 = guardian2
                application.save()
                
                # return redirect('edit_application_form', id=application.id, page=page+1)
        form = ApplicationForm(request.POST, request.FILES, instance=application)
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


def trackApplication(request):
    return render(request, "student/trackApplication.html", {})

# Create your views here.