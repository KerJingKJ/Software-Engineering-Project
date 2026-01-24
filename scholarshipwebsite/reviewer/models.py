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
    
    # Qualitative Scoring Matrix - A. Academic Excellence
    academic_borderline = models.BooleanField(default=False)  # CGPA 3.90-3.91 / Exactly 4As / 8As (UEC) / Exactly 9As (Mix of A/A-)
    academic_competent = models.BooleanField(default=False)   # CGPA 3.92-3.94 / Exactly 9As (High A count)
    academic_superior = models.BooleanField(default=False)    # CGPA 3.95-3.99 / Mix of A+ and A (9+ As)
    academic_elite = models.BooleanField(default=False)       # CGPA 4.00 / 4 A* (A-Level) / Straight A+ (SPM)
    
    # Qualitative Scoring Matrix - B. Academic Rigor & Awards
    rigor_best_student = models.BooleanField(default=False)   # Received "Best Student" / Dean's List / Book Prize award
    rigor_competitions = models.BooleanField(default=False)   # Participated in National/State Academic Competitions
    rigor_none = models.BooleanField(default=False)           # None of the above

    def __str__(self):
        return f"Eligibility Check for {self.application.name}"
