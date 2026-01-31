from django import forms
from .models import Scholarship, ScholarshipCriteria
from django.forms import inlineformset_factory
from datetime import date

class ScholarshipForm(forms.ModelForm):
    # student_type = forms.ChoiceField(choices=[
    #     ('International Student', 'International Student'),
    #     ('Local', 'Local')
    # ], label="Student Type")
    
    # education_level = forms.ChoiceField(choices=[
    #     ('Foundation', 'Foundation'),
    #     ('Undergraduate', 'Undergraduate'),
    #     ('Diploma', 'Diploma'),
    #     ('Postgraduate', 'Postgraduate')
    # ], label="Education Level")

    class Meta:
        model = Scholarship
        fields = ['name', 'description', 'education_level', 'student_type', 'min_gpa', 'notes', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(ScholarshipForm, self).__init__(*args, **kwargs)
    #     if self.instance.pk and self.instance.open_for:
            
    #         parts = self.instance.open_for.split(', ')
    #         if len(parts) >= 2:
    #             self.fields['student_type'].initial = parts[0]
    #             self.fields['education_level'].initial = parts[1]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            
            qs = Scholarship.objects.filter(name=name)
            
            
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError("Scholarship with this name already exists. Please choose a different name.")
        
        return name

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < date.today():
            raise forms.ValidationError("The deadline cannot be in the past.")
        return deadline

    def save(self, commit=True):
        instance = super(ScholarshipForm, self).save(commit=False)
        # student_type = self.cleaned_data.get('student_type')
        # education_level = self.cleaned_data.get('education_level')
        
        instance.open_for = f"{instance.student_type}, {instance.education_level}"
        
        if commit:
            instance.save()
        return instance
    
CriteriaFormSet = inlineformset_factory(
    Scholarship,
    ScholarshipCriteria,
    fields=('qualification', 'requirement', 'entitlement'),
    extra=1,            # Number of empty rows to show by default
    can_delete=True     # Allows checking a box to delete a row
)
