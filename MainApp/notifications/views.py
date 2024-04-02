from django.shortcuts import render, redirect
from .models import Notification, NotificationStatus
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth.decorators import login_required

@login_required(login_url='login1')  # Adjust the 'login1' to your login route as needed
def view_notifications(request):
    if request.method == 'GET':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # It's an AJAX request, send JSON back
            notifications = list(Notification.objects.filter(
                user=request.user, 
                status=NotificationStatus.NOT_READ
            ).order_by('-created_at').values('id', 'message', 'created_at'))

            # Optionally, mark all fetched notifications as read
            Notification.objects.filter(
                user=request.user,
                status=NotificationStatus.NOT_READ
            ).update(status=NotificationStatus.READ)

            # Convert datetime objects to strings for JSON serialization
            for notification in notifications:
                notification['created_at'] = notification['created_at'].isoformat()

            return JsonResponse(notifications, safe=False, encoder=DjangoJSONEncoder)

        # It's a normal GET request, render the full page
        notifications = Notification.objects.filter(
            user=request.user, 
            status=NotificationStatus.NOT_READ
        ).order_by('-created_at').values('id', 'message', 'created_at')

        context = {
            'notifications': notifications,
            'show_messages': True,  # Control the visibility of messages on page load
        }
        return render(request, 'consultantT.html', context)

    elif request.method == 'POST':
        # Mark all notifications as read
        Notification.objects.filter(
            user=request.user, 
            status=NotificationStatus.NOT_READ
        ).update(status=NotificationStatus.READ)

        # Redirect after POST
        return redirect('notifications')  # Adjust 'notifications' to your desired route as needed

    # For other methods, redirect or render another page as needed
    return redirect('consultant')