# forms.py
from django import forms
from .models import Application, Guardian
from datetime import date

# class ApplicationForm(forms.ModelForm):
#     # class Meta:
#     #     model = Application
#     #     fields = ['scholarship', 'submitted_date', 'status', 'interview_status']
#     #     widgets = {
#     #         'submitted_date': forms.DateInput(attrs={'type': 'date'}),
#     #     }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['submitted_date'].required = False
        
#         # Hide status field for new applications (creation)
#         if not self.instance.pk:
#             self.fields['status'].widget = forms.HiddenInput()
#             self.fields['status'].required = False
    
#     # def clean_submitted_date(self):
#     #     submitted_date = self.cleaned_data.get('submitted_date')
#     #     if submitted_date and submitted_date > date.today():
#     #         raise forms.ValidationError(
#     #             "The submitted date cannot be in the future."
#     #         )
#     #     return submitted_date
    
#     # def clean(self):
#     #     cleaned_data = super().clean()
#     #     status = cleaned_data.get('status')
#     #     interview_status = cleaned_data.get('interview_status')
        
#     #     # Validate status and interview_status relationship
#     #     if interview_status == 'Completed' and status != 'Approved':
#     #         raise forms.ValidationError(
#     #             "Interview cannot be marked as completed unless the application is approved."
#     #         )
        
#     #     return cleaned_data
    
#     # def save(self, commit=True):
#     #     instance = super().save(commit=False)
        
#     #     # Auto-set submitted_date if not provided
#     #     if not instance.submitted_date:
#     #         instance.submitted_date = date.today()
        
#     #     # Auto-set status to 'Pending' for new applications
#     #     if not instance.pk: 
#     #         instance.status = 'Pending'
        
#     #     if commit:
#     #         instance.save()
#     #     return instance
    

#     # student_type = forms.ChoiceField(choices=[
#     #     ('International Student', 'International Student'),
#     #     ('Local', 'Local')
#     # ], label="Student Type")
    
#     # education_level = forms.ChoiceField(choices=[
#     #     ('Foundation', 'Foundation'),
#     #     ('Undergraduate', 'Undergraduate'),
#     #     ('Diploma', 'Diploma'),
#     #     ('Postgraduate', 'Postgraduate')
#     # ], label="Education Level")


class ApplicationForm(forms.ModelForm):
    #             'supporting_document', 'personal_achievement', 'reason_deserve',
    #        'ea_form', 'payslip' 
    class Meta:
        model = Application
        fields = [
            'scholarship', 'name', 'home_address', 'correspondence_address',
            'ic_no', 'age', 'date_of_birth', 'intake', 'programme', 'student_identification_number',
            'nationality', 'race', 'gender', 'contact_number', 'email_address','monthly_income',
            'education_level', 'passport_photo', 'academic_result', 
            'personal_achievement', 'supporting_document',
            'reason_deserve', 'ea_form', 'payslip'
        ]
        widgets = {
            'scholarship': forms.Select(attrs={
                'class': 'form-input large-select',
                
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your name',
                
            }),
            'home_address': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                
            }),
            'correspondence_address': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                
            }),
            'ic_no': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Example: 001122143344',
                
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-input small-input',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                
            }),
            'intake': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                
            }),
            'programme': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your programme',
                
            }),
            'student_identification_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Example: 243UC247BR',
                
            }),
            'nationality': forms.Select(attrs={
                'class': 'form-input small-select',
                
            }),
            'race': forms.Select(attrs={
                'class': 'form-input small-select',
                
            }),
            'gender': forms.Select(attrs={
                'class': 'form-input small-select',
                
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Example: 60123456789',
                
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-input',
                
            }),
            'monthly_income': forms.NumberInput(attrs={
                'class': 'form-input medium-input',
                
            }),
            'passport_photo': forms.FileInput(attrs={
                'class': 'file-input',
                
            }),
            'education_level': forms.Select(attrs={
                'class': 'form-input',
                
            }),
            'academic_result': forms.FileInput(attrs={
                'class': 'file-input',
                
            }),
            'personal_achievement': forms.Textarea(attrs={
                'class': 'form-input large-textarea',
                'rows': 8,
                
            }),
            'supporting_document': forms.FileInput(attrs={
                'class': 'file-input',
                'style': 'width: 300px',
            }),
             'reason_deserve': forms.Textarea(attrs={
                'class': 'form-input large-textarea',
                'rows': 10,
            }),
            'ea_form': forms.FileInput(attrs={
                'class': 'file-input',
                'style': 'width: 300px',
            }),
           'payslip': forms.FileInput(attrs={
                'class': 'file-input',
                'style': 'width: 300px',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            

        
        # Make status hidden for new applications (students shouldn't set this)
        if not self.instance.pk:
            # Exclude status field entirely for new applications
            if 'status' in self.fields:
                del self.fields['status']
        
        # Disable scholarship field if already selected
        if self.instance.pk and self.instance.scholarship:
            self.fields['scholarship'].disabled = True

        # Add HTML5 required attribute to required fields
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob >= date.today():
            raise forms.ValidationError("Date of birth must be in the past.")
        return dob
    
    def clean_intake(self):
        intake = self.cleaned_data.get('intake')
        if intake and intake > date.today():
            raise forms.ValidationError("Intake date cannot be in the future.")
        return intake
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 0 or age > 150):
            raise forms.ValidationError("Please enter a valid age.")
        return age
    
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        age = cleaned_data.get('age')
        
        # Verify age matches date of birth
        if dob and age:
            today = date.today()
            calculated_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if abs(calculated_age - age) > 1:
                raise forms.ValidationError("Age doesn't match the date of birth provided.")
        
        return cleaned_data

class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = [
            'relationship', 'name', 'ic_no', 'date_of_birth', 'age',
            'nationality', 'gender', 'address', 'contact_number', 'email_address'
        ]
        widgets = {
            'relationship': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Father, Mother, Guardian',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter guardian name',
            }),
            'ic_no': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Example: 001122143344',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-input small-input',
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter nationality',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-input small-select',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Example: 60123456789',
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-input',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add HTML5 required attribute to required fields
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob >= date.today():
            raise forms.ValidationError("Date of birth must be in the past.")
        return dob
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 0 or age > 150):
            raise forms.ValidationError("Please enter a valid age.")
        return age
    
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        age = cleaned_data.get('age')
        
        # Verify age matches date of birth
        if dob and age:
            today = date.today()
            calculated_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if abs(calculated_age - age) > 1:
                raise forms.ValidationError("Age doesn't match the date of birth provided.")
        
        return cleaned_data