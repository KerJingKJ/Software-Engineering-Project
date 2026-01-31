from django.contrib import admin
from .models import Student, Application, Bookmark, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(Student)
admin.site.register(Notification) # temp create notifs for display

@admin.register(Application)
class ApplicationAssignment(admin.ModelAdmin):
    list_display = ('name', 'scholarship', 'assigned_reviewer', 'assigned_committee_member', 'reviewer_status')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filter for Committee Members
        if db_field.name == "assigned_committee_member":
            kwargs["queryset"] = User.objects.filter(email__icontains='committee.mmu.edu.my')
            
        # Filter for Reviewers
        elif db_field.name == "assigned_reviewer":
            kwargs["queryset"] = User.objects.filter(email__icontains='reviewer.mmu.edu.my')
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Bookmark)

