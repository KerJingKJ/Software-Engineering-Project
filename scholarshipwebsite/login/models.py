from django.db import models
from django.contrib.auth.models import User

# List of 10 security questions choices
SECURITY_QUESTION_CHOICES = [
    ('q1', 'What is the name of your first pet?'),
    ('q2', 'What is your mother\'s maiden name?'),
    ('q3', 'What was the name of your elementary school?'),
    ('q4', 'What is the name of the city where you were born?'),
    ('q5', 'What is your favorite food?'),
    ('q6', 'What is the name of your favorite teacher?'),
    ('q7', 'What is your father\'s middle name?'),
    ('q8', 'What is the make of your first car?'),
    ('q9', 'What is your favorite movie?'),
    ('q10', 'What is your favorite book?'),
]

class UserSecurityQuestion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_questions')
    question_1 = models.CharField(max_length=50, choices=SECURITY_QUESTION_CHOICES)
    answer_1 = models.CharField(max_length=255)
    question_2 = models.CharField(max_length=50, choices=SECURITY_QUESTION_CHOICES)
    answer_2 = models.CharField(max_length=255)

    def __str__(self):
        return f"Security Questions for {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
