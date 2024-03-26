
from django.contrib import admin
from timesheet.models import TimeSheet

@admin.register(TimeSheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time', 'status')

