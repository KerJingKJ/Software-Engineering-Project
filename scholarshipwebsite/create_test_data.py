import os
import django
import sys
from datetime import date

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from committee.models import Scholarship, ScholarshipApplication

def create_test_data():
    print("Creating test data...")
    
    # 1. Create a dummy Scholarship
    scholarship, created = Scholarship.objects.get_or_create(
        name="Engineering Excellence Scholarship",
        defaults={
            'description': "A scholarship for top engineering students.",
            'open_for': "Undergraduate",
            'criteria': "CGPA > 3.5",
            'deadline': date(2025, 12, 31)
        }
    )
    if created:
        print(f"Created Scholarship: {scholarship.name}")
    else:
        print(f"Using existing Scholarship: {scholarship.name}")

    # 2. Create a dummy Application
    app, created = ScholarshipApplication.objects.get_or_create(
        name="Toh Yau Hui",
        scholarship=scholarship,
        defaults={
            'ic_no': '010101-14-1234',
            'email_address': 'student@example.com',
            'date_of_birth': date(2001, 1, 1),
            'age': 23,
            'gender': 'Male',
            'race': 'Chinese',
            'nationality': 'Malaysian',
            'home_address': '123 Jalan Test, Taman Code, 56000 KL',
            'correspondence_address': 'Same as above',
            'contact_number': '012-3456789',
            'intake': date(2023, 9, 1),
            'programme': 'Bachelor of Software Engineering',
            'highest_qualification': 'STPM',
            'personal_achievement': 'Hackathon Winner 2024',
            'reason_deserve': 'I am passionate about coding and need financial support.',
            # File fields will be empty, which is handled in templates with "None"
        }
    )
    
    if created:
        print(f"Created Application for: {app.name} (ID: {app.id})")
    else:
        print(f"Using existing Application for: {app.name} (ID: {app.id})")
        
    print("\n---------------------------------------------------")
    print(f"Test URL: http://127.0.0.1:8000/committee/application/{app.id}/details/")
    print("---------------------------------------------------")

if __name__ == "__main__":
    create_test_data()
