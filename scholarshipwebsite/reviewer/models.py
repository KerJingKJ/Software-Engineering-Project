from django.db import models

# Create your models here.
# from committee.models import ScholarshipApplication
from student.models import Application
from student.models import ScholarshipApplication

class EligibilityCheck(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='eligibility_check')
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
    
    # Qualitative Scoring Matrix - B. Co-Curricular & Leadership
    # Club/Society/Event Highest Position
    leadership_leader = models.BooleanField(default=False)        # Leader (President, Captain, Founder)
    leadership_subleader = models.BooleanField(default=False)     # Sub-leader (Vice-President, Vice-Captain, Co-Founder)
    leadership_secretary = models.BooleanField(default=False)     # Secretary/Treasurer
    leadership_committee = models.BooleanField(default=False)     # Committee Chairs (Social, Marketing, Events)
    leadership_member = models.BooleanField(default=False)        # Member
    
    # B. Co-Curricular & Leadership - 2) Competition/Event Achievement
    competition_national = models.BooleanField(default=False)     # National Level
    competition_state = models.BooleanField(default=False)        # State Level
    competition_university = models.BooleanField(default=False)   # University/District Level
    competition_participant = models.BooleanField(default=False)  # Participant

    # Qualitative Scoring Matrix - C. Personal Statement / Essay Quality
    essay_compelling = models.BooleanField(default=False)     # Unique story, clear goals, specific alignment
    essay_generic = models.BooleanField(default=False)        # Standard answers, lacks specific examples
    essay_poor = models.BooleanField(default=False)           # Grammatical errors, off-topic, or too short

    def __str__(self):
        return f"Eligibility Check for {self.application.name}"

# class placement
class Score(models.Model):
    None
# class placement
class ReviewerAssignment(models.Model):
    None