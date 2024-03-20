
from django.contrib import admin
from timesheet.models import TimeSheet

@admin.register(TimeSheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'clock_in_time', 'clock_out_time', 'status')

