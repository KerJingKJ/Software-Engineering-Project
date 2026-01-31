from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# from student.models import Application, Guardian

class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    open_for = models.CharField(max_length=200)
    education_level = models.CharField(
        max_length=100, 
        default="Undergraduate",
        choices=[
            ('Foundation', 'Foundation'),
            ('Undergraduate', 'Undergraduate'),
            ('Diploma', 'Diploma'),
            ('Postgraduate', 'Postgraduate')
        ]
    )
    student_type = models.CharField(
        max_length=50, 
        default="Local",
        choices=[
            ('International Student', 'International Student'),
            ('Local', 'Local')
        ]
    )
    min_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=3.0,
                                  validators=[
        MinValueValidator(0.0),
        MaxValueValidator(4.0)
    ])
    criteria = models.TextField()
    deadline = models.DateField()

    # def student_type(self):
    #     return self.open_for.split(', ')[0] if self.open_for else ''

    # def education_level(self):
    #     return self.open_for.split(', ')[1] if ', ' in self.open_for else ''
    
    @property
    def status(self):
        return "Open" if self.deadline >= timezone.now().date() else "Closed"

    def __str__(self):
        return self.name

# by hui yee from committe models
class Interview(models.Model):
    application = models.ForeignKey('student.Application', on_delete=models.CASCADE, related_name='interviews')
    date = models.DateField()
    interview_time = models.CharField(max_length=20, default='12:00 PM')  # e.g., "9:00 AM", "10:00 AM"
    timezone = models.CharField(max_length=50)
    # from what i understand, committee would be the ones conducting the interview
    location = models.CharField(max_length=255,default="MMU" )
    remarks = models.TextField(null=True, blank=True)
    committee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Interview for {self.application.name} on {self.date} at {self.interview_time}"

class ApprovedApplication(models.Model):
    """Stores approved student applications with interview details"""
    # Link to original application (optional, for reference)
    original_application = models.ForeignKey('student.Application', on_delete=models.SET_NULL, null=True, blank=True)
    
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


#committee can get the notification too for rescheduled interview
class CommitteeNotification(models.Model):
    # Points to the Committee User (email contains 'committee.mmu.edu.my')
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="committee_alerts"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Alert for {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"