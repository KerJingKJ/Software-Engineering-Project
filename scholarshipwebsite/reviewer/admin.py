from django.contrib import admin
from .models import EligibilityCheck

@admin.register(EligibilityCheck)
class EligibilityCheckAdmin(admin.ModelAdmin):
    list_display = ('application', 'citizenship_check', 'integrity_income_check', 'financial_priority', 'academic_borderline', 'leadership_leader')
