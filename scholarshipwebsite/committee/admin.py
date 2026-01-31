from django.contrib import admin
from .models import Scholarship, Interview, ApprovedApplication
from student.models import Application, Guardian
from .models import Scholarship#, ScholarshipApplication, Guardian, Interview, ApprovedApplication
from .forms import ScholarshipForm
from django.urls import path
from django.template.response import TemplateResponse
from django.urls import reverse

# admin.site.register(ScholarshipApplication)
# admin.site.register(Guardian)
# admin.site.register(Interview)
# admin.site.register(ApprovedApplication)

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    form = ScholarshipForm

def application_dashboard_view(request, extra_context=None):
    total_apps = Application.objects.count()
    approved = Application.objects.filter(committee_status='Approved').count()
    committee_rejected = Application.objects.filter(committee_status='Rejected').count() 
    reviewer_rejected =  Application.objects.filter(reviewer_status='Rejected').count()
    rejected = committee_rejected + reviewer_rejected
    committee_pending = Application.objects.filter(committee_status='Pending').count() 
    pending = committee_pending - reviewer_rejected

    extra_context = extra_context or {}
    extra_context.update({
        'total_apps': total_apps,
        'approved': approved,
        'rejected': rejected,
        'pending': pending,
        # We also need to pass the "api_data" for the charts to work without errors
        # If you haven't created the api_data view yet, the charts will be empty.
    })

    return admin.site.__class__.index(admin.site, request, extra_context)

admin.site.index = application_dashboard_view