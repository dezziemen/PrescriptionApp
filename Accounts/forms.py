import django.forms as forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ('email',)


class PatientRegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=100)
	full_name = forms.CharField(max_length=200)
	address = forms.CharField(max_length=200)
	phone_number = forms.CharField(max_length=10)

	class Meta:
		model = CustomUser
		fields = ["email", "password1", "password2", "full_name", "phone_number", "address", ]
