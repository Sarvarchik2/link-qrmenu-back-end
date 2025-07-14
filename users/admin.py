from django.contrib import admin, messages
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import secrets
import string

class UserAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        if not change and obj.role == 'owner':
            temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
            obj.set_password(temp_password)
            super().save_model(request, obj, form, change)
            self.message_user(request, f"Временный пароль для {obj.username}: {temp_password}", level=messages.WARNING)
        else:
            super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
