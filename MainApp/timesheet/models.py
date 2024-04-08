from django.db import models
from django.conf import settings
from django.utils import timezone

class TimeSheetStatus(models.TextChoices):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    

class TimeSheet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=TimeSheetStatus.choices)
    submission_time = models.DateTimeField()
    def duration(self):
        if self.start_time and self.end_time:
            return (timezone.localtime(self.start_time) - timezone.localtime(self.end_time)).total_seconds() / 3600
        return 0
    
