from audioop import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from timesheet.models import TimeSheet
from django.db.models import ExpressionWrapper, DurationField, Sum, F, Min
from django.db.models.functions import TruncDate

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
    
