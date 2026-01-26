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
        help_text="Current Grade Point Average",
        null=True,
        blank=True,
    )

    course = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Name of the enrolled course"
    )

    year_of_study = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Current year of study"
    )

    student_type = models.CharField(
        max_length=50,
        choices=STUDENT_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Student types, either international student or local"
    )

    education_level = models.CharField(
        max_length=50,
        choices=EDUCATION_LEVEL_CHOICES,
        null=True,
        blank=True,
        help_text="Level of education: foundation, diploma, undergraduate or postgraduate"
    )

    extracurricular_activities = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        help_text="List of extracurricular activities"
    )

    def __str__(self):
        return f"Student {self.user.username}"


# class Application(models.Model):
#     scholarship = models.ForeignKey(
#         Scholarship,
#         on_delete=models.CASCADE,
#         related_name="applications"
#     )

    
#     student = models.ForeignKey(
#         Student,
#         on_delete=models.CASCADE,
#         related_name="applications"
#     )
    
#     submitted_date = models.DateField(
#         default=timezone.now,  # Auto-set to current date
#         help_text="Date when the application was submitted" 
#     )
    
#     status = models.CharField(
#         max_length=50,
#         default='Pending', 
#         help_text="Current status of the application"
#     )
    
#     interview_status = models.CharField(
#         max_length=50,
#         default='Not Scheduled', 
#         help_text="Status of the interview related to application"
#     )

#     class Meta:
#         unique_together = ('student', 'scholarship')
    
#     def __str__(self):
#         return f"Application {self.id} - {self.status}"


    # student_ID = models.CharField(
    #     max_length=50,
    #     help_text="Name of the enrolled course"
    # )

# by hui yee from committe models
class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    submitted_date = models.DateField(         default=timezone.now,  # Auto-set to current date
        help_text="Date when the application was submitted" 
     )
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
    NATIONALITY_CHOICES = [('International Student', 'International Student'),
        ('Local', 'Local')]
    nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES)
    
    RACE_CHOICES = [
        ('Malay', 'Malay'),
        ('Chinese', 'Chinese'),
        ('Indian', 'Indian'),
        ('Other', 'Other'),
    ]
    race = models.CharField(max_length=20, choices=RACE_CHOICES)
    
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    contact_number = models.CharField(max_length=20)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    email_address = models.EmailField()
    QUALIFICATION_CHOICES = choices=[
        ('Foundation', 'Foundation'),
        ('Undergraduate', 'Undergraduate'),
        ('Diploma', 'Diploma'),
        ('Postgraduate', 'Postgraduate')
    ]
    education_level = models.CharField(max_length=200, choices=QUALIFICATION_CHOICES)
    
    # Uploads
    passport_photo = models.ImageField(upload_to='passport_photos/', null=True, blank=True)
    academic_result = models.FileField(upload_to='academic_results/', null=True, blank=True)
    supporting_document = models.FileField(upload_to='supporting_docs/', null=True, blank=True)
    
    personal_achievement = models.TextField(null=True, blank=True)
    reason_deserve = models.TextField(null=True, blank=True)
    ea_form = models.FileField(upload_to='ea_forms/',null=True, blank=True)
    payslip = models.FileField(upload_to='payslips/',null=True, blank=True)

    class Meta:
        db_table = 'student_application'

    def __str__(self):
        return f"{self.name} - {self.scholarship.name}"

# by hui yee from committe models
class Guardian(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='guardians')
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

    class Meta:
        db_table = 'student_guardian'

    def __str__(self):
        return f"{self.name} ({self.relationship}) - {self.application.name}"


# by hui yee from committe models
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
    

# class EligibilityCheck(models.Model):
#     application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='eligibility_check')
#     citizenship_check = models.BooleanField(default=False)
#     programme_level_check = models.BooleanField(default=False)
    
#     # Qualifying Exam
#     exam_foundation_spm = models.BooleanField(default=False)
#     exam_degree_stpm_uec = models.BooleanField(default=False)
#     exam_degree_matriculation = models.BooleanField(default=False)
    
#     # Minimum Grades
#     grade_spm = models.BooleanField(default=False)
#     grade_stpm = models.BooleanField(default=False)
#     grade_uec = models.BooleanField(default=False)
#     grade_foundation = models.BooleanField(default=False)
    
#     documents_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Eligibility Check for {self.application.name}"


# by hui yee from committe models
# Not sure why we need this? Shouldnt these details be stored in interview?