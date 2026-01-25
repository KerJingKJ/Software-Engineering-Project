from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    open_for = models.CharField(max_length=200)
    criteria = models.TextField()
    deadline = models.DateField()

    def student_type(self):
        return self.open_for.split(', ')[0] if self.open_for else ''

    def education_level(self):
        return self.open_for.split(', ')[1] if ', ' in self.open_for else ''
    
    @property
    def status(self):
        return "Open" if self.deadline >= timezone.now().date() else "Closed"

    def __str__(self):
        return self.name



from student.models import ScholarshipApplication, Guardian


class Interview(models.Model):
    application = models.ForeignKey(ScholarshipApplication, on_delete=models.CASCADE, related_name='interviews')
    date = models.DateField()
    interview_time = models.CharField(max_length=20, default='12:00 PM')
    timezone = models.CharField(max_length=50)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Interview for {self.application.name} on {self.date} at {self.interview_time}"

class ApprovedApplication(models.Model):
    
    original_application = models.ForeignKey(ScholarshipApplication, on_delete=models.SET_NULL, null=True, blank=True)
    
    scholarship_name = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    ic_no = models.CharField(max_length=20)
    email_address = models.EmailField()
    contact_number = models.CharField(max_length=20)
    programme = models.CharField(max_length=200)
    
    interview_date = models.DateField()
    interview_time = models.CharField(max_length=20)
    interview_timezone = models.CharField(max_length=50)
    
    approved_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'approved_applications'

    def __str__(self):
        return f"{self.student_name} - {self.scholarship_name} (Approved)"
