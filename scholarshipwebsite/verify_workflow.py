import os
import django
import sys
from datetime import date
from decimal import Decimal

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from committee.models import Scholarship, ScholarshipApplication, Guardian, Interview, ApprovedApplication

def run_verification():
    print("=======================================================")
    print("      STARTING COMMITTEE WORKFLOW VERIFICATION")
    print("=======================================================")

    # 1. Setup Test Data
    print("\n[1] Setting up test data...")
    user = User.objects.filter(username='committee_test').first()
    if not user:
        user = User.objects.create_user('committee_test', 'test@example.com', 'password123')
        print("    Created test user: committee_test")
    else:
        print("    Using existing test user: committee_test")

    scholarship, _ = Scholarship.objects.get_or_create(
        name="Test Scholarship",
        defaults={
            'description': 'Test Desc',
            'open_for': 'Everyone',
            'criteria': 'None',
            'deadline': date.today()
        }
    )
    
    # Create Application for Approval Test
    app_approve = ScholarshipApplication.objects.create(
        scholarship=scholarship,
        name="Alice Approver",
        ic_no="999999-99-9999",
        date_of_birth=date(1999, 1, 1),
        age=25,
        gender="Female",
        nationality="Malaysian",
        race="Chinese",
        home_address="123 Test St",
        correspondence_address="123 Test St",
        email_address="alice@example.com",
        contact_number="0123456789",
        highest_qualification="Degree",
        programme="CS",
        intake="Jan 2025",
        status='Pending'
    )
    Guardian.objects.create(application=app_approve, name="Dad", relationship="Father", monthly_income=1000)
    print(f"    Created App for Approval: {app_approve.name} (ID: {app_approve.id})")

    # Create Application for Rejection Test
    app_reject = ScholarshipApplication.objects.create(
        scholarship=scholarship,
        name="Bob Rejecter",
        ic_no="888888-88-8888",
        date_of_birth=date(1998, 2, 2),
        age=26,
        gender="Male",
        nationality="Malaysian",
        race="Malay",
        home_address="456 Test Ave",
        correspondence_address="456 Test Ave",
        email_address="bob@example.com",
        contact_number="9876543210",
        highest_qualification="Diploma",
        programme="IT",
        intake="Jan 2025",
        status='Pending'
    )
    print(f"    Created App for Rejection: {app_reject.name} (ID: {app_reject.id})")

    client = Client()
    # client.force_login(user) # If login was required, but currently views seem open or handle anon

    # ==============================================================================
    # TEST CASE A: APPROVE FLOW
    # ==============================================================================
    print("\n[2] Testing APPROVE Flow (Alice)...")
    
    # 2.1 View Details
    url_details = reverse('view_application_details', args=[app_approve.id])
    resp = client.get(url_details)
    if resp.status_code == 200:
        print("    [PASS] View Application Details page loaded.")
    else:
        print(f"    [FAIL] View Application Details page failed. Status: {resp.status_code}")

    # 2.2 View Family
    url_family = reverse('view_family_background', args=[app_approve.id])
    resp = client.get(url_family)
    if resp.status_code == 200:
        print("    [PASS] View Family Background page loaded.")
    else:
        print(f"    [FAIL] View Family Background page failed. Status: {resp.status_code}")

    # 2.3 Schedule Interview
    print("    Scheduling Interview...")
    url_interview = reverse('schedule_interview', args=[app_approve.id])
    resp = client.post(url_interview, {
        'date': date.today().strftime('%Y-%m-%d'),
        'interview_time': '10:00 AM',
        'timezone': 'GMT+8'
    })
    
    if Interview.objects.filter(application=app_approve).exists():
        print("    [PASS] Interview created in database.")
    else:
        print("    [FAIL] Interview NOT found in database.")

    # 2.4 Approve Decision
    print("    Approving Application...")
    url_decision = reverse('decision_page', args=[app_approve.id])
    resp = client.post(url_decision, {'decision': 'Approved'})
    
    app_approve.refresh_from_db()
    if app_approve.status == 'Approved':
        print(f"    [PASS] Application status updated to '{app_approve.status}'.")
    else:
        print(f"    [FAIL] Application status is '{app_approve.status}', expected 'Approved'.")

    # Check ApprovedApplication table
    approved_record = ApprovedApplication.objects.filter(original_application=app_approve).first()
    if approved_record:
        print(f"    [PASS] ApprovedApplication record created for {approved_record.student_name}.")
        print(f"           Interview Time Copied: {approved_record.interview_time}")
    else:
        print("    [FAIL] ApprovedApplication record NOT created.")

    # ==============================================================================
    # TEST CASE B: REJECT FLOW
    # ==============================================================================
    print("\n[3] Testing REJECT Flow (Bob)...")

    # 3.1 Schedule Interview (Optional but good to test persistence)
    Interview.objects.create(
        application=app_reject,
        date=date.today(),
        interview_time="2:00 PM",
        timezone="UTC"
    )
    
    # 3.2 Reject Decision
    print("    Rejecting Application...")
    url_decision = reverse('decision_page', args=[app_reject.id])
    resp = client.post(url_decision, {'decision': 'Rejected'})

    # 3.3 Verify Data Persistence (Revert Logic Check)
    try:
        app_reject.refresh_from_db()
        print(f"    [PASS] Application still exists (not deleted).")
        
        if app_reject.status == 'Rejected':
             print(f"    [PASS] Application status updated to '{app_reject.status}'.")
        else:
             print(f"    [FAIL] Application status is '{app_reject.status}', expected 'Rejected'.")

        if Interview.objects.filter(application=app_reject).exists():
             print("    [PASS] Interview record still exists.")
        else:
             print("    [FAIL] Interview record was DELETED (Unexpected).")

    except ScholarshipApplication.DoesNotExist:
        print("    [FAIL] Application was DELETED from database (User requested NON-delete logic).")

    print("\n=======================================================")
    print("      VERIFICATION COMPLETE")
    print("=======================================================")

if __name__ == "__main__":
    run_verification()
