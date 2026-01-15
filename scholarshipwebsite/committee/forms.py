from django import forms
from .models import Scholarship
from datetime import date

class ScholarshipForm(forms.ModelForm):
    student_type = forms.ChoiceField(choices=[
        ('International Student', 'International Student'),
        ('Local', 'Local')
    ], label="Student Type")
    
    education_level = forms.ChoiceField(choices=[
        ('Foundation', 'Foundation'),
        ('Undergraduate', 'Undergraduate'),
        ('Diploma', 'Diploma'),
        ('Postgraduate', 'Postgraduate')
    ], label="Education Level")

    class Meta:
        model = Scholarship
        fields = ['name', 'description', 'criteria', 'deadline'] # removed open_for
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ScholarshipForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.open_for:
            # Try to split open_for assuming format "Type, Level"
            parts = self.instance.open_for.split(', ')
            if len(parts) >= 2:
                self.fields['student_type'].initial = parts[0]
                self.fields['education_level'].initial = parts[1]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check if a scholarship with this name exists
            qs = Scholarship.objects.filter(name=name)
            
            # If editing an existing instance, exclude it from the check
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
        student_type = self.cleaned_data.get('student_type')
        education_level = self.cleaned_data.get('education_level')
        # Combine the fields
        instance.open_for = f"{student_type}, {education_level}"
        
        if commit:
            instance.save()
        return instance
