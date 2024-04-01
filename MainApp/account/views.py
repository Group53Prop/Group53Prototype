from audioop import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from timesheet.models import TimeSheet, TimeSheetStatus
from django.db.models import ExpressionWrapper, DurationField, Sum, F, Min, Max
from django.db.models.functions import TruncDate, TruncDay
from timesheet.models import TimeSheet
from .forms import  TimeSheetStatusUpdateForm
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware,get_default_timezone
from notifications.models import Notification


def login_view(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['loginUser']  
        password = request.POST['loginPassword']  
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            session_id = request.session.session_key
            return redirect('account:portal') 
        else:
            context['error'] = 'Invalid credentials'  
    return render(request, 'login1.html', {'just_logged_in': True}) 

def logout_redirect(request):
    logout(request)
    return render(request,'login1.html')

def portal_view(request):
    user_type = None
    if request.user.is_authenticated:
        user_type = request.user.user_type  
    return render(request, 'newPortal.html', {'user_type': user_type})

def my_view(request):
    context = {
        'user_name': request.user.first_name, 
    }
    return render(request, 'newPortal.html', context)

def consultant_view(request):
    return render(request, 'ConsultantT.html')

def financial_view(request):
    return render(request, 'FinancialT.html')

def manager_view(request):
    return render(request, 'LineManagerT.html')

def view_today_timesheet(request):
    
    if not request.user.is_authenticated:

        return render(request, 'login1.html')

    
    today_start = timezone.localdate()
    today_end = timezone.localdate()

    
    todays_timesheets = TimeSheet.objects.filter(
        user=request.user,
        start_time__date=today_start,
        end_time__date=today_end
    )

    total_duration = todays_timesheets.annotate(
        duration=ExpressionWrapper(
            F('end_time') - F('start_time'),
            output_field=DurationField()
        )
    ).aggregate(total=Sum('duration'))

    total_seconds = total_duration['total'].total_seconds() if total_duration['total'] else 0
    total_hours = total_seconds / 3600  

    context = {
        'todays_timesheets': todays_timesheets,
        'current_day': today_start.strftime("%A, %B %d, %Y"),
        'total_hours': "{:.2f}".format(total_hours),  
    }

    return render(request, 'viewTimeSheet.html', context)

def view_past_timesheets(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    today = timezone.localdate()
    past_timesheets = (
        TimeSheet.objects
        .filter(user=request.user, start_time__lt=today)
        .annotate(date=TruncDate('start_time'))  
        .values('date')  
        .annotate(
            total_duration=Sum(
                ExpressionWrapper(
                    F('end_time') - F('start_time'),
                    output_field=DurationField()
                )
            ),
            status=Min('status') 
        )
        .order_by('-date')  
    )
    for timesheet in past_timesheets:
        timesheet['total_seconds'] = timesheet['total_duration'].total_seconds() if timesheet['total_duration'] else 0
        timesheet['total_hours'] = timesheet['total_seconds'] / 3600

    return render(request, 'timesheethistory.html', {'past_timesheets': past_timesheets})



@login_required
def redirect_based_on_user_type(request):
    user_type = request.user.user_type  
    
    if user_type == 'consultant':
        return redirect('consultant')
    elif user_type == 'financeteam':
        return redirect('financial')
    else:
        return redirect('manager')




@login_required
def view_timesheets(request):
    if request.method == 'POST':
        form = TimeSheetStatusUpdateForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            date = form.cleaned_data['date']
            timesheets_to_update = TimeSheet.objects.filter(start_time__date=date)

            # First, update the status of the timesheets
            updated_count = timesheets_to_update.update(status=new_status)

            if updated_count > 0:
                # Assuming 'date' is a date object, format it as needed for the notification
                formatted_date = date.strftime("%Y-%m-%d")  # Adjust the format as needed

                # Fetch unique users from the timesheets to update
                users_to_notify = set(ts.user for ts in timesheets_to_update)

                # Create a single notification per user
                notifications = [
                    Notification(
                        user=user,
                        created_by=request.user,
                        message=f'Your timesheet on {formatted_date} has been {new_status.lower()}.'
                    ) for user in users_to_notify
                ]
                Notification.objects.bulk_create(notifications)

            return redirect('view_timesheets')
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)

    # Handle GET request
    today = timezone.localdate()
    timesheets = TimeSheet.objects.filter(start_time__lt=today).exclude(start_time__date=today)

    timesheets_grouped = timesheets.annotate(
        date=TruncDay('start_time')
    ).values(
        'user', 'user__first_name', 'user__last_name', 'user__email', 'date'
    ).annotate(
        total_duration=Sum(ExpressionWrapper(F('end_time') - F('start_time'), output_field=DurationField())),
        status=Min('status')
    ).order_by('user', '-date')

    grouped_data = []
    for group in timesheets_grouped:
        user_id = group['user']
        date = group['date']
        total_seconds = group['total_duration'].total_seconds() if group['total_duration'] else 0
        total_hours = "{:.2f}".format(total_seconds / 3600)
        
        clock_entries = TimeSheet.objects.filter(
            user_id=user_id,
            start_time__date=date
        ).values('id', 'start_time', 'end_time')

        grouped_data.append({
            'user_id': user_id,
            'user_info': f"{group['user__first_name']} {group['user__last_name']}",
            'user_email': group['user__email'],
            'date': date,
            'total_hours': total_hours,
            'status': group['status'],
            'clock_ins_outs': list(clock_entries)
        })
    
    return render(request, 'viewtimesheetmanager.html', {
        'timesheets_grouped': grouped_data,
        'status_choices': TimeSheetStatus.choices,
    })

def parse_datetime(time_str, date_str):
    try:
        return datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
    except ValueError as e:
        print(f"Error parsing datetime: {e}")
        return None

@login_required
def update_timesheet_entry(request):
    if request.method == 'POST':
        print(f"POST data: {request.POST}")
        entry_id = request.POST.get('entry_id')
        print(f"Entry ID: {entry_id}")

        if entry_id:
            start_time_str = request.POST.get(f'start_time_{entry_id}')
            end_time_str = request.POST.get(f'end_time_{entry_id}')
            date_str = request.POST.get('date')
            
            start_time = parse_datetime(start_time_str, date_str)
            end_time = parse_datetime(end_time_str, date_str)

            if not start_time or not end_time:
                messages.error(request, "Invalid time format.")
                return redirect('account:view_timesheets')

            if end_time <= start_time:
                messages.error(request, "End time cannot be before start time.")
                return redirect('account:view_timesheets')
                
            start_time = make_aware(start_time)
            end_time = make_aware(end_time)

        try:
            entry = get_object_or_404(TimeSheet, pk=entry_id)
            
            # Add a check to confirm that the end_time is after the start_time
            if end_time <= start_time:
                messages.error(request, "The end time must be after the start time.")
                return redirect('account:view_timesheets')

            change_reason = request.POST.get('change_reason')  # Retrieve the change reason from POST data
            if not change_reason:
                messages.error(request, "You must provide a reason for the change.")
                return redirect('account:view_timesheets')

            # Now we update the entry with the new times and reason
            entry.start_time = start_time
            entry.end_time = end_time
            entry.change_reason = change_reason  # Assuming you have a field for reason
            entry.save()

            # Create a notification message
            notification_message = f"Your timesheet clocks have been changed: Clock-in at {start_time.strftime('%H:%M')}, clock-out at {end_time.strftime('%H:%M')}. Reason: {change_reason}"

            # Create a notification in the database
            Notification.objects.create(
                user=entry.user,
                created_by=request.user,
                message=notification_message
            )
            
            messages.success(request, 'TimeSheet entry updated successfully.')
        except Exception as e:
            messages.error(request, f'An error occurred while updating the timesheet entry: {e}')

        return redirect('account:view_timesheets')

    return redirect('account:view_timesheets')