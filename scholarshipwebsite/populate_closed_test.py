import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from committee.models import Scholarship

def populate():
    # Create a Closed Scholarship (Deadline in the past)
    past_date = date.today() - timedelta(days=1)
    scholarship, created = Scholarship.objects.get_or_create(
        name="Expired Scholarship (Closed Test)",
        defaults={
            'description': 'This scholarship has ended and should not be clickable.',
            'open_for': 'Local',
            'deadline': past_date,
            'notes': 'Test notes for expired scholarship'
        }
    )
    if created:
        print(f"Created Closed Scholarship: {scholarship.name} (Deadline: {scholarship.deadline})")
    else:
        # Update existing one to be closed just in case
        scholarship.deadline = past_date
        scholarship.save()
        print(f"Updated existing Scholarship to Closed: {scholarship.name} (Deadline: {scholarship.deadline})")

if __name__ == "__main__":
    populate()
