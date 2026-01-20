from django.db import models
from django.utils import timezone
# Create your models here.
class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    open_for = models.CharField(max_length=200)
    criteria = models.TextField()
    deadline = models.DateField()

    def student_type(self):
        return self.open_for.split(', ')[0] if self.open_for else ''

    def education_level(self):
        return self.open_for.split(', ')[1] if ', ' in self.open_for else ''
    
    @property
    def status(self):
        return "Open" if self.deadline >= timezone.now().date() else "Closed"

    def __str__(self):
        return self.name
