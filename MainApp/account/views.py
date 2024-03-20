from audioop import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


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

    return render(request, 'login1.html', context) 

def logout_view(request):
    logout(request)
    return redirect('account:login') 

def logout_redirect(request):
    return render(request,'login1.html')

def portal_view(request):
    return render(request, 'newPortal.html')

def my_view(request):
    context = {
        'user_name': request.user.first_name, 
    }
    return render(request, 'newPortal.html', context)