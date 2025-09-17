from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class USERAdmin(UserAdmin):
    list_display = ["id", "username", "email", "is_staff"]


admin.site.register(User, USERAdmin)
