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

    a_count = models.PositiveIntegerField(null=True, blank=True)

    qualification = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="e.g. SPM, STPM, UEC, Foundation"
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


# by hui yee from committe models
class Guardian(models.Model):
    # application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='guardians')
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
        return f"{self.name} ({self.relationship})"


# by hui yee from committe models
class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    REVIEWER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Rejected', 'Rejected'),
    ]

    COMMITTEE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    ACCEPTANCE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    
    acceptance_status = models.CharField(
        max_length=20, 
        choices=ACCEPTANCE_STATUS_CHOICES, 
        default='Pending',
        help_text="Student's decision after committee approval"
    )
    submitted_date = models.DateField(         default=timezone.now,  # Auto-set to current date
        help_text="Date when the application was submitted" 
     )
    reviewer_status = models.CharField(max_length=20, choices=REVIEWER_STATUS_CHOICES, default='Pending')
    committee_status = models.CharField(max_length=20, choices=COMMITTEE_STATUS_CHOICES, default='Pending')
    iscomplete = models.BooleanField(default=False)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    home_address = models.TextField()
    correspondence_address = models.TextField()
    ic_no = models.CharField(max_length=20)
    age = models.IntegerField()
    date_of_birth = models.DateField()
    intake = models.DateField()
    programme = models.CharField(max_length=200)
    student_identification_number = models.CharField(max_length=20)
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
    EDUCATION_LEVEL_CHOICES = [
        ('Foundation', 'Foundation'),
        ('Undergraduate', 'Undergraduate'),
        ('Diploma', 'Diploma'),
        ('Postgraduate', 'Postgraduate')
    ]

    education_level = models.CharField(
        max_length=50,
        choices=EDUCATION_LEVEL_CHOICES,
        null=True,    # Important: Allows existing rows to be empty without crashing
        blank=True,
        help_text="Level of education snapshot at time of application"
    )
    # 1. Define the choices for Previous Qualification
    PREVIOUS_QUALIFICATION_CHOICES = [
        ('SPM', 'SPM'),
        ('STPM', 'STPM'),
        ('UEC', 'UEC'),
        ('Matriculation', 'Matriculation'),
        ('Foundation', 'Foundation'),
        ('Diploma', 'Diploma'),
        ('A-Level', 'A-Level'),
        ('IB', 'International Baccalaureate'),
        ('Other', 'Other'),
    ]

    # 2. Add the field
    highest_qualification = models.CharField(
        max_length=50,
        choices=PREVIOUS_QUALIFICATION_CHOICES,
        null=True,     # Allow null initially to avoid migration errors on existing rows
        blank=True,
        help_text="The highest academic qualification you have completed (e.g. STPM, UEC)"
    )
    # Uploads
    passport_photo = models.ImageField(upload_to='passport_photos/', null=True, blank=True)
    academic_result = models.FileField(upload_to='academic_results/', null=True, blank=True)
    supporting_document = models.FileField(upload_to='supporting_docs/', null=True, blank=True)

    personal_achievement = models.TextField(null=True, blank=True)
    reason_deserve = models.TextField(null=True, blank=True)
    guardian1 = models.ForeignKey(Guardian, on_delete=models.CASCADE,null=True, blank=True, related_name='guardian1')
    guardian2 = models.ForeignKey(Guardian, on_delete=models.CASCADE,null=True, blank=True, related_name='guardian2')
    ea_form = models.FileField(upload_to='ea_forms/',null=True, blank=True)
    payslip = models.FileField(upload_to='payslips/',null=True, blank=True)

    assigned_reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_reviews'
    )
    assigned_committee_member = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_committee_tasks'
    )
    
    class Meta:
        db_table = 'student_application'

    def __str__(self):
        return f"{self.name} - {self.scholarship.name}"

    def save(self, *args, **kwargs):
        # Get all nullable fields
        nullable_fields = [
            field.name for field in self._meta.get_fields()
            if hasattr(field, 'null') and field.null and hasattr(field, 'blank') and field.blank
        ]
        
        # Check if all nullable fields have values
        all_fields_filled = all(
            getattr(self, field) for field in nullable_fields
        )
        
        # Update iscomplete based on completeness
        self.iscomplete = all_fields_filled
        
        # Call the parent save method
        super().save(*args, **kwargs)

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
        ordering = ['-date_added']

    def __str__(self):
        return f"Bookmark {self.id} - {self.date_added}"


class Notification(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    NOTIFICATION_TYPES = [
        ("Application", "Application"),
        ("System", "System"),
        ("Reminder", "Reminder"),
    ]

    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default="System"
    )

    message = models.TextField(help_text="Notification message content" )
    is_read = models.BooleanField(default=False)
    display_at = models.DateTimeField(
        default=timezone.now,  # default to current datetime
        help_text="Date the notification should be displayed" 
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # Auto-set to current datetime
        help_text="Date when the notification was created" 
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_type_display()} for {self.student} - {self.created_at}"