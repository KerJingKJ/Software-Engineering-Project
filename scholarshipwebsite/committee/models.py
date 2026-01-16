from django.db import models

# Create your models here.
class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    open_for = models.CharField(max_length=200)
    criteria = models.TextField()
    deadline = models.DateField()

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class ScholarshipApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    home_address = models.TextField()
    correspondence_address = models.TextField()
    ic_no = models.CharField(max_length=20)
    age = models.IntegerField()
    date_of_birth = models.DateField()
    intake = models.DateField()
    programme = models.CharField(max_length=200)
    nationality = models.CharField(max_length=100)
    
    RACE_CHOICES = [
        ('Malay', 'Malay'),
        ('Chinese', 'Chinese'),
        ('India', 'India'),
    ]
    race = models.CharField(max_length=20, choices=RACE_CHOICES)
    
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    contact_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    highest_qualification = models.CharField(max_length=200)
    
    # Uploads
    passport_photo = models.ImageField(upload_to='passport_photos/')
    academic_result = models.FileField(upload_to='academic_results/')
    supporting_document = models.FileField(upload_to='supporting_docs/')
    
    personal_achievement = models.TextField()
    reason_deserve = models.TextField()
    
    # These were requested in the second page but seem to belong to the application generally or maybe specific to guardians?
    # The prompt says "upload两个file一个是ea form和latest 3 months payslip" on the second page (family background).
    # Since there are two guardians, but usually EA form/payslip is per household or per guardian? 
    # The prompt says "upload two files... on the second page is family background". 
    # Usually these documents are proof of income for the parents/guardians.
    # I will put them on the Application model as requested by the structure "second page is family background... and need upload two files".
    # If it was per guardian, it would be in Guardian model. But usually it's attached to the application overall as "documents".
    # However, since they are financial docs, putting them on Application makes sense for "Family" proof.
    ea_form = models.FileField(upload_to='ea_forms/')
    payslip = models.FileField(upload_to='payslips/')

    class Meta:
        db_table = 'student_scholarship_application'

    def __str__(self):
        return f"{self.name} - {self.scholarship.name}"

class Guardian(models.Model):
    application = models.ForeignKey(ScholarshipApplication, on_delete=models.CASCADE, related_name='guardians')
    relationship = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    ic_no = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    nationality = models.CharField(max_length=100)
    
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'student_guardian'

    def __str__(self):
        return f"{self.name} ({self.relationship}) - {self.application.name}"

class Interview(models.Model):
    application = models.ForeignKey(ScholarshipApplication, on_delete=models.CASCADE, related_name='interviews')
    date = models.DateField()
    interview_time = models.CharField(max_length=20, default='12:00 PM')  # e.g., "9:00 AM", "10:00 AM"
    timezone = models.CharField(max_length=50)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Interview for {self.application.name} on {self.date} at {self.interview_time}"

class ApprovedApplication(models.Model):
    """Stores approved student applications with interview details"""
    # Link to original application (optional, for reference)
    original_application = models.ForeignKey(ScholarshipApplication, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Student Info (copied from ScholarshipApplication)
    scholarship_name = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    ic_no = models.CharField(max_length=20)
    email_address = models.EmailField()
    contact_number = models.CharField(max_length=20)
    programme = models.CharField(max_length=200)
    
    # Interview Info (copied from Interview)
    interview_date = models.DateField()
    interview_time = models.CharField(max_length=20)
    interview_timezone = models.CharField(max_length=50)
    
    # Approval Info
    approved_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'approved_applications'

    def __str__(self):
        return f"{self.student_name} - {self.scholarship_name} (Approved)"
