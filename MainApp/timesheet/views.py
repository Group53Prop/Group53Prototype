from django.shortcuts import render
import json
from django.db import transaction
import logging
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import TimeSheet, TimeSheetStatus



def my_view(request):
    return render(request, 'login1.html')

@require_POST
@login_required
def clock_in(request):
    data = json.loads(request.body)

    if data.get('action') == 'clock_in':
        # Assuming that 'start_time' and 'submission_time' should be set to the current time
        # and 'end_time' could be the end of the workday or similar, you'll need to decide.
        # The status is set to PENDING as a default.
        new_timesheet = TimeSheet.objects.create(
            user=request.user,
            start_time=timezone.now(),
            end_time=timezone.now(),
            status=TimeSheetStatus.PENDING,
            submission_time=timezone.now()
        )

        # You might want to format the response with more details, e.g., the ID of the new timesheet
        return JsonResponse({
            'status': 'success',
            'msg': 'Clock in recorded',
            'timesheet_id': new_timesheet.id
        })

    return JsonResponse({'status': 'error', 'msg': 'Invalid action'}, status=400)




@require_POST
@login_required
def clock_out(request):
    data = json.loads(request.body)

    if data.get('action') == 'clock_out':
        with transaction.atomic():
            try:
                latest_timesheet = TimeSheet.objects.select_for_update().filter(
                    user=request.user,
                    status=TimeSheetStatus.PENDING
                ).latest('start_time')

                latest_timesheet.end_time = timezone.now()
                latest_timesheet.status = TimeSheetStatus.PENDING
                latest_timesheet.save()

                return JsonResponse({
                    'status': 'success',
                    'msg': 'Clock out recorded',
                    'timesheet_id': latest_timesheet.id
                })

            except TimeSheet.DoesNotExist:
                return JsonResponse({'status': 'error', 'msg': 'No pending timesheet found'}, status=404)
            except Exception as e:  # This is to catch any other exceptions that might be occurring
                logging.exception("Error occurred when trying to clock out.")  # Make sure logging is imported
                return JsonResponse({'status': 'error', 'msg': 'An unexpected error occurred'}, status=500)

    return JsonResponse({'status': 'error', 'msg': 'Invalid action'}, status=400)

