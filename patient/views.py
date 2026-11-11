from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout




# Home / Registration
def index(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'index.html', {'form': form})



# Login
def userlogin(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user= authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'error_message': error_message})  
        return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return redirect('login')    


# Dashboard

def dashboard(request):
    return render(request, 'dashboard.html')


# Profile

def profile(request):
    return render(request, 'profile.html')


# Book Appointment

def bookappointment(request):
    return render(request, 'bookappointment.html')


