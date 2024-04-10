from django.contrib import admin
from .models import Profile, Subscribe

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_birth', 'photo']
    raw_id_fields = ['user'] #change display default list users in admin dashboard

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to']