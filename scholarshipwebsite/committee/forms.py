from django import forms
from .models import Scholarship

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['name', 'description', 'open_for', 'criteria', 'deadline']
