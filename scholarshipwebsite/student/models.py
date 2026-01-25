# models.py
from django.db import models
from django.utils import timezone
from django.conf import settings
from committee.models import Scholarship
from django.contrib.auth.models import User

class Student(models.Model):
    STUDENT_TYPE_CHOICES = [
        ('International Student', 'International Student'),
        ('Local', 'Local')
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('Foundation', 'Foundation'),
        ('Undergraduate', 'Undergraduate'),
        ('Diploma', 'Diploma'),
        ('Postgraduate', 'Postgraduate')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')

    current_gpa = models.FloatField(
        help_text="Current Grade Point Average"
    )

    course = models.CharField(
        max_length=50,
        help_text="Name of the enrolled course"
    )

    year_of_study = models.PositiveSmallIntegerField(
        help_text="Current year of study"
    )

    student_type = models.CharField(
        max_length=50,
        choices=STUDENT_TYPE_CHOICES,
        help_text="Student types, either international student or local"
    )

    education_level = models.CharField(
        max_length=50,
        choices=EDUCATION_LEVEL_CHOICES,
        help_text="Level of education: foundation, diploma, undergraduate or postgraduate"
    )

    extracurricular_activities = models.TextField(
        max_length=200,
        blank=True,
        help_text="List of extracurricular activities"
    )

    def __str__(self):
        return f"Student {self.user.username}"


class Application(models.Model):
    scholarship = models.ForeignKey(
        Scholarship,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    
    submitted_date = models.DateField(
        default=timezone.now,  # Auto-set to current date
        help_text="Date when the application was submitted" 
    )
    
    status = models.CharField(
        max_length=50,
        default='Pending', 
        help_text="Current status of the application"
    )
    
    interview_status = models.CharField(
        max_length=50,
        default='Not Scheduled', 
        help_text="Status of the interview related to application"
    )

    class Meta:
        unique_together = ('student', 'scholarship')
    
    def __str__(self):
        return f"Application {self.id} - {self.status}"

class Bookmark(models.Model):
    scholarship = models.ForeignKey(
        Scholarship,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    
    date_added = models.DateField(
        default=timezone.now,  # Auto-set to current date
        help_text="Date when the bookmark was added" 
    )

    class Meta:
        unique_together = ('student', 'scholarship')

    def __str__(self):
        return f"Bookmark {self.id} - {self.date_added}"
