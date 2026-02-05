from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
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
   
    notes = models.TextField()
    deadline = models.DateField()
    def get_notes_list(self):
        """Splits the notes into a list based on new lines."""
        # This splits the text line by line and removes empty lines
        return [note.strip() for note in self.notes.splitlines() if note.strip()]
       
    @property
    def status(self):
        return "Open" if self.deadline >= timezone.now().date() else "Closed"

    def __str__(self):
        return self.name

class ScholarshipCriteria(models.Model):
    CRITERIA_TYPE_CHOICES = [
        ('GPA', 'Minimum GPA'),
        ('A_COUNT', 'Number of As'),
        ('TEXT', 'Text Only / Manual'),
    ]

    QUALIFICATION_CHOICES = [
    ('SPM', 'SPM'),
    ('STPM/A-Level', 'STPM/A-Level'),
    ('UEC', 'UEC'),
    ('Foundation', 'Foundation/Matriculation'),
    ('Diploma', 'Diploma'),
    ('Undergraduate', 'Undergraduate Degree'),
    ]

    scholarship = models.ForeignKey(
        Scholarship,
        on_delete=models.CASCADE,
        related_name='criteria_list'
    )

    qualification = models.CharField(
        max_length=100,
        choices=QUALIFICATION_CHOICES
    )

    criteria_type = models.CharField(
        max_length=20,
        choices=CRITERIA_TYPE_CHOICES
    )

    min_value = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
        MinValueValidator(Decimal('0.00'))
    ],
    help_text="GPA or number of As (0.00 – 4.00)"
    )

    entitlement = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.qualification} - {self.scholarship.name}"

class Interview(models.Model):
    application = models.ForeignKey('student.Application', on_delete=models.CASCADE, related_name='interviews')
    date = models.DateField()
    interview_time = models.CharField(max_length=20, default='12:00 PM')  # e.g., "9:00 AM", "10:00 AM"
    timezone = models.CharField(max_length=50)
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