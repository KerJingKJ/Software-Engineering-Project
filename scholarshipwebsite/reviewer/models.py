from django.db import models

# Create your models here.
from committee.models import ScholarshipApplication

class EligibilityCheck(models.Model):
    application = models.OneToOneField(ScholarshipApplication, on_delete=models.CASCADE, related_name='eligibility_check')
    citizenship_check = models.BooleanField(default=False)
    programme_level_check = models.BooleanField(default=False)
    
    # Qualifying Exam
    exam_foundation_spm = models.BooleanField(default=False)
    exam_degree_stpm_uec = models.BooleanField(default=False)
    exam_degree_matriculation = models.BooleanField(default=False)
    
    # Minimum Grades
    grade_spm = models.BooleanField(default=False)
    grade_stpm = models.BooleanField(default=False)
    grade_uec = models.BooleanField(default=False)
    grade_foundation = models.BooleanField(default=False)
    
    documents_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Eligibility Check for {self.application.name}"
