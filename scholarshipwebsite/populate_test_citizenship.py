import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from django.contrib.auth.models import User
from committee.models import Scholarship
from student.models import Student, Application
from django.utils import timezone
from datetime import date
from decimal import Decimal

try:
    # 1. Get or create a reviewer user
    user, created = User.objects.get_or_create(username='huiyee', defaults={'email': 'huiyee@reviewer.com'})
    if created:
        user.set_password('Mnbv@1234')
        user.save()
        print("Reviewer 'huiyee' created.")
    else:
        print("Reviewer 'huiyee' already exists.")

    # 2. Get or create a scholarship
    scholarship, created = Scholarship.objects.get_or_create(
        name="Test Scholarship for Citizenship Check",
        defaults={
            'description': 'Test description',
            'open_for': 'All',
            'deadline': date(2026, 12, 31),
            'notes': 'Test notes'
        }
    )
    if created: print("Scholarship created.")
    else: print("Scholarship already exists.")

    # 3. Create a Local Student
    local_student_user, created = User.objects.get_or_create(username='local_student', defaults={'email': 'local@student.com'})
    if created: local_student_user.set_password('password123'); local_student_user.save()
    local_student, created = Student.objects.get_or_create(user=local_student_user)
    
    local_app, created = Application.objects.get_or_create(
        name='Ahmad Malaysian',
        defaults={
            'student': local_student,
            'scholarship': scholarship,
            'nationality': 'Local',
            'ic_no': '010101-10-1234',
            'age': 20,
            'date_of_birth': date(2005, 1, 1),
            'intake': date(2025, 9, 1),
            'programme': 'Bachelor of IT',
            'student_identification_number': '1211101234',
            'race': 'Malay',
            'gender': 'Male',
            'contact_number': '012-3456789',
            'monthly_income': Decimal('3000.00'),
            'email_address': 'local@student.com',
            'home_address': 'Kuala Lumpur',
            'correspondence_address': 'Kuala Lumpur',
            'assigned_reviewer': user
        }
    )
    if created: print(f"Local App created (ID: {local_app.id})")
    else: print(f"Local App already exists (ID: {local_app.id})")

    # 4. Create an International Student
    intl_student_user, created = User.objects.get_or_create(username='intl_student', defaults={'email': 'intl@student.com'})
    if created: intl_student_user.set_password('password123'); intl_student_user.save()
    intl_student, created = Student.objects.get_or_create(user=intl_student_user)
    
    intl_app, created = Application.objects.get_or_create(
        name='John International',
        defaults={
            'student': intl_student,
            'scholarship': scholarship,
            'nationality': 'International Student',
            'ic_no': 'A12345678',
            'age': 21,
            'date_of_birth': date(2004, 5, 15),
            'intake': date(2025, 9, 1),
            'programme': 'Bachelor of CS',
            'student_identification_number': '1211105678',
            'race': 'Other',
            'gender': 'Male',
            'contact_number': '019-8765432',
            'monthly_income': Decimal('8000.00'),
            'email_address': 'intl@student.com',
            'home_address': 'London, UK',
            'correspondence_address': 'London, UK',
            'assigned_reviewer': user
        }
    )
    if created: print(f"International App created (ID: {intl_app.id})")
    else: print(f"International App already exists (ID: {intl_app.id})")

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
