
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from student.models import ScholarshipApplication
from committee.models import Scholarship

def test_approval():
    # Create a dummy scholarship if needed
    scholarship, _ = Scholarship.objects.get_or_create(name="Test Scholarship")
    
    import datetime
    # Create a dummy application
    app = ScholarshipApplication.objects.create(
        scholarship=scholarship,
        name="Test Applicant",
        ic_no="123456",
        email_address="test@example.com",
        contact_number="0123456789",
        age=20,
        date_of_birth=datetime.date(2000, 1, 1),
        intake=datetime.date(2023, 1, 1),
        programme="CS",
        nationality="Test",
        race="Malay",
        gender="Male",
        highest_qualification="STPM",
        status="Pending",
        submitted_date=datetime.date.today(), # Ensure this is compatible with the model
        passport_photo="test.jpg",
        academic_result="test.pdf",
        supporting_document="test.pdf",
        personal_achievement="None",
        reason_deserve="None",
        ea_form="test.pdf",
        payslip="test.pdf",
        home_address="Test Address",
        correspondence_address="Test Address"
    )
    
    print(f"Initial status: {app.status}")
    
    # Simulate approval logic
    app.status = "Approved"
    app.save()
    
    # Refresh from db
    app.refresh_from_db()
    print(f"Post-save status: {app.status}")
    
    if app.status == "Approved":
        print("SUCCESS: Status updated correctly.")
    else:
        print("FAILURE: Status did not update.")

if __name__ == "__main__":
    test_approval()
