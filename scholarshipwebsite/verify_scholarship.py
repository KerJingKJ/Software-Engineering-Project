import os
import django
from django.test import Client
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from committee.models import Scholarship

def verify():
    with open('verify_log.txt', 'w') as f:
        c = Client()
        f.write("Sending POST request to create scholarship...\n")
        response = c.post('/committee/create/', {
            'name': 'Test Scholarship 2',
            'description': 'A test scholarship 2',
            'open_for': 'Undergraduates',
            'criteria': 'GPA > 3.0',
            'deadline': '2025-01-01'
        })
        
        f.write(f"Response status code: {response.status_code}\n")
        f.write(f"Response content: {response.content.decode()}\n")
        
        if response.status_code == 200 and "Scholarship created successfully" in response.content.decode():
            f.write("Success response received.\n")
        else:
            f.write("Failed to get success response.\n")
            
        f.write("Checking database...\n")
        s = Scholarship.objects.filter(name='Test Scholarship 2').first()
        if s:
            f.write(f"Scholarship found in DB: {s.name}, {s.deadline}\n")
        else:
            f.write("Scholarship NOT found in DB.\n")

if __name__ == "__main__":
    verify()
