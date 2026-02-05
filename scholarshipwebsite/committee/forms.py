from django import forms
from .models import Scholarship, ScholarshipCriteria
from django.forms import inlineformset_factory
from datetime import date

class ScholarshipForm(forms.ModelForm):

    class Meta:
        model = Scholarship
        fields = ['name', 'description', 'education_level', 'student_type', 'notes', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

# check to make sure no duplicated scholarship names
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            
            qs = Scholarship.objects.filter(name=name)
            
            
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError("Scholarship with this name already exists. Please choose a different name.")
        
        return name

# check deadlines cannot be in past
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < date.today():
            raise forms.ValidationError("The deadline cannot be in the past.")
        return deadline

    def save(self, commit=True):
        instance = super(ScholarshipForm, self).save(commit=False)
        
        instance.open_for = f"{instance.student_type}, {instance.education_level}"
        
        if commit:
            instance.save()
        return instance
    
CriteriaFormSet = inlineformset_factory(
    Scholarship,
    ScholarshipCriteria,
    fields=('qualification', 'criteria_type', 'min_value', 'entitlement'),
    extra=1,            # Number of empty rows to show by default
    can_delete=True     # Allows checking a box to delete a row
)
