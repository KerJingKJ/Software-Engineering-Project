
from django import forms
from .models import Application
from datetime import date

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['scholarship', 'submitted_date', 'status', 'interview_status']
        widgets = {
            'submitted_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['submitted_date'].required = False
        
        
        if not self.instance.pk:
            self.fields['status'].widget = forms.HiddenInput()
            self.fields['status'].required = False
    
    def clean_submitted_date(self):
        submitted_date = self.cleaned_data.get('submitted_date')
        if submitted_date and submitted_date > date.today():
            raise forms.ValidationError("Submitted date cannot be in the future.")
        return submitted_date
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        interview_status = cleaned_data.get('interview_status')
        
        if interview_status == 'Completed' and status != 'Approved':
            raise forms.ValidationError("Interview must be completed for approved applications.")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        
        if not instance.submitted_date:
            instance.submitted_date = date.today()
        
        
        if not instance.pk: 
            instance.status = 'Pending'
        
        if commit:
            instance.save()
        return instance
    

    
    
    
    
    
    
    
    
    
    
    