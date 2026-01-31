from django.contrib import admin
from .models import Scholarship, Interview, ApprovedApplication, ScholarshipCriteria
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

class ScholarshipCriteriaInline(admin.TabularInline):
    model = ScholarshipCriteria
    extra = 1
    
@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    form = ScholarshipForm
    inlines = [ScholarshipCriteriaInline]

def application_dashboard_view(request, extra_context=None):
    # Gather metrics
    total_apps = Application.objects.count()
    approved = Application.objects.filter(committee_status='Approved').count()
    rejected = Application.objects.filter(committee_status='Rejected').count()
    pending = Application.objects.exclude(committee_status__in=['Approved', 'Rejected']).count()

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