import os
import django
import sys
from datetime import date
from decimal import Decimal

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from committee.models import Scholarship, ScholarshipApplication, Guardian

def create_new_applicant():
    print("Creating NEW test applicant...")
    
    # 1. Get or Create Scholarship
    scholarship, _ = Scholarship.objects.get_or_create(
        name="Merit Scholarship 2025",
        defaults={
            'description': 'For top students',
            'open_for': 'High Achievers',
            'criteria': '3.5 CGPA',
            'deadline': date(2025, 12, 31)
        }
    )

    # 2. Create New Application
    app = ScholarshipApplication.objects.create(
        scholarship=scholarship,
        name="Siti Aminah",
        ic_no="020520-10-1234",
        date_of_birth=date(2002, 5, 20),
        age=23,
        gender="Female",
        nationality="Malaysian",
        race="Malay",
        home_address="789 Jalan Bunga, Shah Alam, 40000 Selangor",
        correspondence_address="789 Jalan Bunga, Shah Alam, 40000 Selangor",
        contact_number="019-9988776",
        email_address="siti.aminah@example.com",
        highest_qualification="STPM",
        programme="Bachelor of Software Engineering",
        intake=date(2024, 9, 1),
        personal_achievement="Debate Club President, State Level Runner-up",
        reason_deserve="I have a strong passion for coding and need financial aid.",
        status='Pending'
    )
    print(f"Created Application: {app.name} (ID: {app.id})")

    # 3. Create Guardians
    Guardian.objects.create(
        application=app,
        relationship='Father',
        name="Abdul Rahman",
        ic_no="650101-10-5555",
        date_of_birth=date(1965, 1, 1),
        age=60,
        nationality='Malaysian',
        gender='Male',
        address='789 Jalan Bunga, Shah Alam',
        contact_number='019-1122334',
        email_address='rahman@example.com',
        monthly_income=Decimal('4500.00')
    )
    
    Guardian.objects.create(
        application=app,
        relationship='Mother',
        name="Fatimah binti Ali",
        ic_no="680202-10-6666",
        date_of_birth=date(1968, 2, 2),
        age=57,
        nationality='Malaysian',
        gender='Female',
        address='789 Jalan Bunga, Shah Alam',
        contact_number='019-2233445',
        email_address='fatimah@example.com',
        monthly_income=Decimal('2500.00')
    )
    print("Created Guardians for Siti Aminah.")

    print("\n---------------------------------------------------")
    print(f"NEW Test URL: http://127.0.0.1:8000/committee/application/{app.id}/details/")
    print("---------------------------------------------------")

if __name__ == "__main__":
    create_new_applicant()
