import os
import django
import random
from datetime import date, timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from django.contrib.auth.models import User
from committee.models import Scholarship, Interview, ApprovedApplication
from student.models import Student, Application, Guardian
from reviewer.models import EligibilityCheck

def create_mock_data():
    # 1. Create a Committee User
    committee_user, _ = User.objects.get_or_create(username='committee_test', defaults={'is_staff': True})
    committee_user.set_password('password123')
    committee_user.save()

    # 2. Create Scholarships
    s1, _ = Scholarship.objects.get_or_create(
        name='Future Leaders Scholarship 2026',
        defaults={
            'description': 'Awarded to students with exceptional leadership potential.',
            'open_for': 'Local, Undergraduate',
            'education_level': 'Undergraduate',
            'student_type': 'Local',
            'min_gpa': 3.5,
            'criteria': 'Active involvement in leadership roles.',
            'deadline': date.today() + timedelta(days=30)
        }
    )

    s2, _ = Scholarship.objects.get_or_create(
        name='Global Excellence Award',
        defaults={
            'description': 'For high-achieving international students.',
            'open_for': 'International Student, Postgraduate',
            'education_level': 'Postgraduate',
            'student_type': 'International Student',
            'min_gpa': 3.8,
            'criteria': 'Academic excellence and research potential.',
            'deadline': date.today() + timedelta(days=15)
        }
    )

    # 3. Create Students and Applications
    names = ['John Doe', 'Jane Smith', 'Ali bin Ahmad', 'Lee Wei', 'Sarah Connor']
    
    for i, name in enumerate(names):
        username = name.lower().replace(' ', '_')
        user, _ = User.objects.get_or_create(username=username)
        user.set_password('password123')
        user.save()

        student, _ = Student.objects.get_or_create(
            user=user,
            defaults={
                'current_gpa': round(3.5 + (random.random() * 0.5), 2),
                'course': 'Computer Science',
                'year_of_study': random.randint(1, 4),
                'student_type': 'Local' if i < 3 else 'International Student',
                'education_level': 'Undergraduate' if i < 4 else 'Postgraduate'
            }
        )

        # Create Application
        scholarship = s1 if i < 4 else s2
        status = 'Reviewed' if i % 2 == 0 else 'Pending'
        committee_status = 'Pending'
        
        app, created = Application.objects.get_or_create(
            student=student,
            scholarship=scholarship,
            defaults={
                'name': name,
                'home_address': f'{10 + i}, Mock Street, City',
                'correspondence_address': f'{10 + i}, Mock Street, City',
                'ic_no': f'000000-00-000{i}',
                'age': 20 + i,
                'date_of_birth': date(2000, 1, 1),
                'intake': date(2025, 1, 1),
                'programme': 'BSc Computer Science',
                'student_identification_number': f'ID{1000 + i}',
                'nationality': 'Local' if i < 3 else 'International Student',
                'race': 'Malay' if i == 2 else ('Chinese' if i == 3 else 'Other'),
                'gender': 'Male' if i % 2 == 0 else 'Female',
                'contact_number': f'012-345678{i}',
                'monthly_income': 5000 + (i * 1000),
                'email_address': f'{username}@example.com',
                'education_level': 'Undergraduate',
                'reviewer_status': status,
                'committee_status': committee_status,
                'assigned_committee_member': committee_user
            }
        )

        if created:
            # Create Guardian
            g = Guardian.objects.create(
                relationship='Father',
                name=f'Guardian of {name}',
                ic_no=f'600000-00-000{i}',
                date_of_birth=date(1970, 1, 1),
                age=55,
                nationality='Malaysian',
                gender='Male',
                address=app.home_address,
                contact_number=app.contact_number,
                email_address=f'guardian_{i}@example.com'
            )
            app.guardian1 = g
            app.save()

            # Create EligibilityCheck for Reviewed ones
            if status == 'Reviewed':
                EligibilityCheck.objects.create(
                    application=app,
                    citizenship_check=True,
                    programme_level_check=True,
                    documents_verified=True,
                    academic_superior=True,
                    leadership_committee=True,
                    essay_compelling=True,
                    integrity_income_check=True,
                    financial_priority='3',
                    total_marks=85,
                    reviewer_comment='Excellent candidate with strong leadership profile.'
                )
                
                # Create a mock interview for some
                if i == 0:
                    Interview.objects.create(
                        application=app,
                        date=date.today() + timedelta(days=5),
                        interview_time='10:00 AM',
                        timezone='MYT',
                        location='Room 101, Admin Building',
                        remarks='Please bring original IC/Passport.',
                        committee=committee_user
                    )

    print("Successfully populated mock data!")

if __name__ == "__main__":
    create_mock_data()
