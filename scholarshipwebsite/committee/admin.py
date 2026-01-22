from django.contrib import admin

from .models import Scholarship, Interview, ApprovedApplication
from student.models import ScholarshipApplication, Guardian
from .models import Scholarship#, ScholarshipApplication, Guardian, Interview, ApprovedApplication
from .forms import ScholarshipForm


# admin.site.register(ScholarshipApplication)
# admin.site.register(Guardian)
# admin.site.register(Interview)
# admin.site.register(ApprovedApplication)

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    form = ScholarshipForm

