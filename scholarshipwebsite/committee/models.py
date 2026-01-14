from django.db import models

# Create your models here.
class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    open_for = models.CharField(max_length=200)
    criteria = models.TextField()
    deadline = models.DateField()

    def __str__(self):
        return self.name
