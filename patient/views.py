from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from patient.forms import PatientForm
from patient.models import Patient
from django.shortcuts import render, redirect, get_object_or_404
from patient.models import Patient
from patient.forms import PatientForm



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
    patients = Patient.objects.all()
    return render(request, 'dashboard.html', {'patients': patients})


# Profile

def profile(request):
    return render(request, 'profile.html')


# Book Appointment

def bookappointment(request):
    return render(request, 'bookappointment.html')

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})  

def view_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    return render(request, 'view_patient.html', {
        'patient': patient
    })


def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = PatientForm(instance=patient)

    return render(request, 'edit_patient.html', {
        'form': form,
        'patient': patient
    })


def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        patient.delete()
        return redirect('dashboard')

    return render(request, 'delete_patient.html', {
        'patient': patient
    })

