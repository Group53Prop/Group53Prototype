from django.db import models
from django.conf import settings


class NotificationStatus(models.TextChoices):
    READ = 'Read'
    NOT_READ = 'Not Read'
    

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_notifications', on_delete=models.SET_NULL, null=True, blank=True)
    status=status = models.CharField(max_length=10  , choices=NotificationStatus.choices, default='Not Read')
