from django.db import models
# Create your models here.
# from committee.models import ScholarshipApplication
from student.models import Application

class EligibilityCheck(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='eligibility_check')
    citizenship_check = models.BooleanField(default=False)
    programme_level_check = models.BooleanField(default=False)
    
    
    exam_foundation_spm = models.BooleanField(default=False)
    exam_degree_stpm_uec = models.BooleanField(default=False)
    exam_degree_matriculation = models.BooleanField(default=False)
    
    
    grade_spm = models.BooleanField(default=False)
    grade_stpm = models.BooleanField(default=False)
    grade_uec = models.BooleanField(default=False)
    grade_foundation = models.BooleanField(default=False)
    
    documents_verified = models.BooleanField(default=False)
    
    
    academic_borderline = models.BooleanField(default=False)  
    academic_competent = models.BooleanField(default=False)   
    academic_superior = models.BooleanField(default=False)    
    academic_elite = models.BooleanField(default=False)       
    
    
    rigor_best_student = models.BooleanField(default=False)   
    rigor_competitions = models.BooleanField(default=False)   
    rigor_none = models.BooleanField(default=False)           
    
    
    
    leadership_leader = models.BooleanField(default=False)        
    leadership_subleader = models.BooleanField(default=False)     
    leadership_secretary = models.BooleanField(default=False)     
    leadership_committee = models.BooleanField(default=False)     
    leadership_member = models.BooleanField(default=False)        
    
    
    competition_national = models.BooleanField(default=False)     
    competition_state = models.BooleanField(default=False)        
    competition_university = models.BooleanField(default=False)   
    competition_participant = models.BooleanField(default=False)  

    
    essay_compelling = models.BooleanField(default=False)     
    essay_generic = models.BooleanField(default=False)        
    essay_poor = models.BooleanField(default=False)           

    
    
    integrity_income_check = models.BooleanField(default=False) 

    
    FINANCIAL_PRIORITY_CHOICES = [
        ('1', '(1) Low Need (T20)'),
        ('2', '(2) Moderate Need (M40)'),
        ('3', '(3) High Need (B40)'),
        ('4', '(4) Critical Need (B40)'),
    ]
    financial_priority = models.CharField(max_length=2, choices=FINANCIAL_PRIORITY_CHOICES, blank=True, null=True)

    
    hardship_single_income = models.BooleanField(default=False)
    hardship_large_family = models.BooleanField(default=False)
    hardship_retiree = models.BooleanField(default=False)
    hardship_medical = models.BooleanField(default=False)

    
    total_marks = models.IntegerField(default=0)
    reviewer_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Eligibility Check for {self.application.name}"

# class placement
class Score(models.Model):
    None
# class placement
class ReviewerAssignment(models.Model):
    None