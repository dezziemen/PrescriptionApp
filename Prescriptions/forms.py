import django.forms as forms
from .models import Prescription, MedicineQuantity, Medicine


class PrescriptionCreationForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['date', 'doctor', 'pharmacist', 'patient', 'collected']


class MedicineQuantityCreationForm(forms.ModelForm):
    class Meta:
        model = MedicineQuantity
        fields = ['medicine', 'quantity']


class MedicineCreationForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'tablets', 'volume']
