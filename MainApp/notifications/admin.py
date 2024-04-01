from django.contrib import admin
from .models import Notification  # Import your Notification model

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_by', 'message', 'created_at')  # Adjust the fields to match your model
    search_fields = ('user__username', 'created_by__username', 'message') 