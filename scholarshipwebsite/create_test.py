import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from committee.models import Scholarship
from student.models import ScholarshipApplication, Guardian
from datetime import date

# Get or create a scholarship
scholarship, created = Scholarship.objects.get_or_create(
    name="Engineering Excellence Scholarship",
    defaults={
        'description': "For outstanding engineering students",
        'open_for': "Local, Undergraduate",
        'criteria': "CGPA 3.5 and above",
        'deadline': date(2026, 12, 31)
    }
)
print(f"Scholarship: {scholarship.name} (created: {created})")

# Create a test application
app, created = ScholarshipApplication.objects.get_or_create(
    name="Toh Yau Hui",
    defaults={
        'scholarship': scholarship,
        'status': 'Pending',
        'home_address': '123 Main Street, KL',
        'correspondence_address': '123 Main Street, KL',
        'ic_no': '010101-01-0101',
        'age': 20,
        'date_of_birth': date(2005, 1, 1),
        'intake': date(2024, 9, 1),
        'programme': 'Bachelor of Engineering',
        'nationality': 'Malaysian',
        'race': 'Chinese',
        'gender': 'Male',
        'contact_number': '012-3456789',
        'email_address': 'tyh@example.com',
        'highest_qualification': 'A-Level',
        'passport_photo': 'passport_photos/test.jpg',
        'academic_result': 'academic_results/test.pdf',
        'supporting_document': 'supporting_docs/test.pdf',
        'personal_achievement': 'Dean List for 3 semesters',
        'reason_deserve': 'Strong academic performance',
        'ea_form': 'ea_forms/test.pdf',
        'payslip': 'payslips/test.pdf'
    }
)
print(f"Application: {app.name} (created: {created})")

# Create guardian
guardian, created = Guardian.objects.get_or_create(
    application=app,
    name="Father",
    defaults={
        'relationship': 'Father',
        'ic_no': '700101-01-0101',
        'date_of_birth': date(1970, 1, 1),
        'age': 55,
        'nationality': 'Malaysian',
        'gender': 'Male',
        'address': '123 Main Street, KL',
        'contact_number': '012-9876543',
        'email_address': 'father@example.com',
        'monthly_income': 5000.00
    }
)
print(f"Guardian: {guardian.name} (created: {created})")

print("\nTest data created successfully!")
