from django.contrib import admin

from .models import UserSecurityQuestion, UserProfile

admin.site.register(UserSecurityQuestion)
admin.site.register(UserProfile)
