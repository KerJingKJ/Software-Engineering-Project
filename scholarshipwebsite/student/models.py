
from django.db import models
from django.utils import timezone
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



from committee.models import Scholarship


class ScholarshipApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
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
    nationality = models.CharField(max_length=100)
    
    RACE_CHOICES = [
        ('Malay', 'Malay'),
        ('Chinese', 'Chinese'),
        ('India', 'India'),
    ]
    race = models.CharField(max_length=20, choices=RACE_CHOICES)
    
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    contact_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    highest_qualification = models.CharField(max_length=200)
    
    
    passport_photo = models.ImageField(upload_to='passport_photos/')
    academic_result = models.FileField(upload_to='academic_results/')
    supporting_document = models.FileField(upload_to='supporting_docs/')
    
    personal_achievement = models.TextField()
    reason_deserve = models.TextField()
    
    ea_form = models.FileField(upload_to='ea_forms/')
    payslip = models.FileField(upload_to='payslips/')
    
    submitted_date = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'student_scholarship_application'

    def __str__(self):
        return f"{self.name} - {self.scholarship.name}"


class Guardian(models.Model):
    application = models.ForeignKey(ScholarshipApplication, on_delete=models.CASCADE, related_name='guardians')
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
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'student_guardian'

    def __str__(self):
        return f"{self.name} ({self.relationship}) - {self.application.name}"


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
        default=timezone.now,
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
        default=timezone.now,
        help_text="Date when the bookmark was added" 
    )

    class Meta:
        unique_together = ('student', 'scholarship')

    def __str__(self):
        return f"Bookmark {self.id} - {self.date_added}"
