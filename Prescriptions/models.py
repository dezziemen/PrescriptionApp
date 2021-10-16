import datetime
from Accounts.models import CustomUser
from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    tablets = models.IntegerField()
    volume = models.FloatField()

    def __str__(self):
        return self.name


class MedicineQuantity(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.quantity) + ' ' + str(self.medicine)


class Prescription(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    doctor = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='doctor')
    pharmacist = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='pharmacist')
    patient = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='patient')
    collected = models.BooleanField(default=False)

    def __str__(self):
        return 'Collected by ' if self.collected else 'Prescribed to ' + str(self.patient) + ' on ' + str(self.date)
