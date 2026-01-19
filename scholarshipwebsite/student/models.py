# models.py
from django.db import models
from django.utils import timezone
from committee.models import Scholarship

class Application(models.Model):
    scholarship = models.ForeignKey(
        Scholarship,
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
    
    def __str__(self):
        return f"Application {self.id} - {self.status}"