from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,JobSeeker,Employee,Job,Application,EmailRecord
from django.utils.html import format_html

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model=CustomUser
    list_display=('username','email','user_type','is_staff','is_active')
    list_filter=('user_type','is_staff','is_superuser','is_active')
    search_fields=('username','email','user_type')
    ordering=('username',)


fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'firstname', 'lastname', 'number','dp_thumbnail')
    def dp_thumbnail(self, obj):
        if obj.dp:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 0%;" />', obj.dp.url)
        return "No photo uploaded"
    dp_thumbnail.short_description = 'Profile Picture'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'companyname', 'companyindustry','logo_thumbnail')
    def logo_thumbnail(self,obj):
        if obj.companylogo:
            return format_html('<img src={} width="50 height="50" style="object-fit: cover; border-radius: 0%;" />', obj.companylogo.url)
        return "No logo uploaded"
    logo_thumbnail.short_description='Company Logo'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'location', 'salary_range', 'application_deadline', 'posted_by')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'jobseeker', 'applied_at')


@admin.register(EmailRecord)
class EmailRecordAdmin(admin.ModelAdmin):
    list_display = ('jobseeker', 'job', 'action', 'subject', 'sent_at')
