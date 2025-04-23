from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task

# Custom UserAdmin to show role in admin
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role',)

# Task Admin
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee', 'date', 'hours_spent', 'status')
    list_filter = ('status', 'date', 'employee')
    search_fields = ('title', 'description', 'employee__username')
    readonly_fields = ('status',)
    ordering = ('-date',)

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
