from django.contrib import admin

from .models import Scholarship, ScholarshipApplication, Guardian, Interview, ApprovedApplication

admin.site.register(Scholarship)
admin.site.register(ScholarshipApplication)
admin.site.register(Guardian)
admin.site.register(Interview)
admin.site.register(ApprovedApplication)
