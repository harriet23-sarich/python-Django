from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout

from patient.forms import PatientForm
from patient.models import Patient, Payment
from patient.serializers import PatientSerializer

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.contrib import messages
from django_daraja.mpesa.core import MpesaClient



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

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            error_message = "Invalid username or password."

            return render(
                request,
                'login.html',
                {'error_message': error_message}
            )

    return render(request, 'login.html')


# Logout
def logout(request):
    auth_logout(request)
    return redirect('login')


# Dashboard
def dashboard(request):
    patients = Patient.objects.all()

    return render(
        request,
        'dashboard.html',
        {'patients': patients}
    )


# Profile
def profile(request):
    return render(request, 'profile.html')


# Book Appointment
def bookappointment(request):
    return render(request, 'bookappointment.html')


# Add Patient
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = PatientForm()

    return render(
        request,
        'add_patient.html',
        {'form': form}
    )


# View Patient
def view_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    return render(
        request,
        'view_patient.html',
        {'patient': patient}
    )


# Edit Patient
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        form = PatientForm(
            request.POST,
            instance=patient
        )

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        'edit_patient.html',
        {
            'form': form,
            'patient': patient
        }
    )


# Delete Patient
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        patient.delete()
        return redirect('dashboard')

    return render(
        request,
        'delete_patient.html',
        {'patient': patient}
    )


# REST API
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]

def make_payment(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        phone_number = request.POST.get('phone_number')
        amount = float(request.POST.get('amount'))

        
        payment = Payment.objects.create(
            patient_name=patient_name,
            phone_number=phone_number,
            amount=amount
        )

        cl = MpesaClient()
        account_reference = "Hospital Payment"
        transaction_desc = "Payment for hospital services"
        callback_url = "https://example.com/callback" 
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        payment.transaction_id = response['CheckoutRequestID']
        payment.save()
        messages.success(request, 'Payment initiated successfully. Please complete the payment on your phone')
    

        return redirect('dashboard')  

    return render(request, 'make_payment.html')