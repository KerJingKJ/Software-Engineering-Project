from django.contrib import admin

from .models import Scholarship

from .forms import ScholarshipForm

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    form = ScholarshipForm
