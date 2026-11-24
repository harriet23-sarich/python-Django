from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.patient_id   


class Payment(models.Model):
    patientname = models.CharField(max_length=100)
    account = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment{self.transaction_id} for {self.patientname}"