from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'role', 'is_verified', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'phone_number')
    ordering = ('created_at',)
    list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('profile_picture', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'phone_number')}
        ),
    )

    filter_horizontal = ('groups', 'user_permissions')

    # Use email instead of username for Django admin login
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

admin.site.register(User, CustomUserAdmin)
