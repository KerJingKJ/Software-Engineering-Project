from django.contrib import admin
from .models import Student, Application, Bookmark

#register this two function so that i can check the application whether is it working
admin.site.register(Student)
admin.site.register(Application)
admin.site.register(Bookmark)