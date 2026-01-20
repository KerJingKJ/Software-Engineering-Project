import os
import django
import sys
import urllib.request
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarshipwebsite.settings')
django.setup()

from committee.models import ScholarshipApplication

def add_test_image():
    print("Downloading test image...")
    image_url = "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg"
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                image_content = response.read()
                print("Image downloaded successfully.")
                
                # Get the applicant (ID 2 or 1)
                try:
                    app = ScholarshipApplication.objects.get(pk=2)
                    print("Found applicant: Siti Aminah (ID 2)")
                except ScholarshipApplication.DoesNotExist:
                    app = ScholarshipApplication.objects.first()
                    print(f"ID 2 not found, using first applicant: {app.name} (ID {app.id})")
                
                # Save image
                app.passport_photo.save("test_cat.jpg", ContentFile(image_content), save=True)
                print("Image saved to passport_photo field.")
                
                print("\n---------------------------------------------------")
                print(f"Check image at: http://127.0.0.1:8000/committee/application/{app.id}/details/")
                print("---------------------------------------------------")
            else:
                print(f"Failed to download image. Status: {response.status}")
    except Exception as e:
        print(f"Error downloading image: {e}")

if __name__ == "__main__":
    add_test_image()
