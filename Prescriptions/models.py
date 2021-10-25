import datetime
from django.core.validators import MinValueValidator

from Accounts.models import CustomUser
from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    tablets = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    volume = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class Prescription(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    doctor = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='doctor')
    pharmacist = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='pharmacist', blank=True, null=True)
    patient = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='patient')
    collected = models.BooleanField(default=False)

    def __str__(self):
        return 'Collected by ' if self.collected else 'Prescribed to ' + str(self.patient) + ' on ' + str(self.date)


class MedicineCart(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_cart')

    def __str__(self):
        return f'{self.patient} medicine cart'


class MedicineQuantity(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.DO_NOTHING, default=None, blank=True, null=True)
    medicine_cart = models.ForeignKey(MedicineCart, on_delete=models.DO_NOTHING, default=None, blank=True, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.quantity) + ' ' + str(self.medicine)
