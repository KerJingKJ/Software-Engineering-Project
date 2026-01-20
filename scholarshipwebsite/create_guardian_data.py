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

def create_test_data():
    print("Creating test data...")
    
    # 1. Get existing application
    try:
        app = ScholarshipApplication.objects.get(name="Toh Yau Hui")
        print(f"Found Application: {app.name} (ID: {app.id})")
    except ScholarshipApplication.DoesNotExist:
        print("Application not found. Please run create_test_data.py first.")
        return

    # 2. Create Guardian 1
    guardian1, created = Guardian.objects.get_or_create(
        application=app,
        name="Toh Ah Kow",
        defaults={
            'relationship': 'Father',
            'ic_no': '701215-14-5678',
            'date_of_birth': date(1970, 12, 15),
            'age': 55,
            'nationality': 'Malaysian',
            'gender': 'Male',
            'address': '123 Jalan Test, Taman Code, 56000 KL',
            'contact_number': '012-1234567',
            'email_address': 'father@example.com',
            'monthly_income': Decimal('5000.00'),
        }
    )
    if created:
        print(f"Created Guardian 1: {guardian1.name}")
    else:
        print(f"Using existing Guardian 1: {guardian1.name}")

    # 3. Create Guardian 2
    guardian2, created = Guardian.objects.get_or_create(
        application=app,
        name="Lim Mei Ling",
        defaults={
            'relationship': 'Mother',
            'ic_no': '721020-14-9876',
            'date_of_birth': date(1972, 10, 20),
            'age': 53,
            'nationality': 'Malaysian',
            'gender': 'Female',
            'address': '123 Jalan Test, Taman Code, 56000 KL',
            'contact_number': '012-7654321',
            'email_address': 'mother@example.com',
            'monthly_income': Decimal('3500.00'),
        }
    )
    if created:
        print(f"Created Guardian 2: {guardian2.name}")
    else:
        print(f"Using existing Guardian 2: {guardian2.name}")

    print("\n---------------------------------------------------")
    print(f"Test URL: http://127.0.0.1:8000/committee/application/{app.id}/family/")
    print("---------------------------------------------------")

if __name__ == "__main__":
    create_test_data()
