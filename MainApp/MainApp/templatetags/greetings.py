from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag(takes_context=True)
def time_based_greeting(context):
    current_time = timezone.localtime(timezone.now())
    if current_time.hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_time.hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= current_time.hour < 20:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"
    user_name = context['user'].first_name if context['user'].first_name else "User"
    return f"{greeting}, {user_name}"
