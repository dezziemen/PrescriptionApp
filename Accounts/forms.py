import django.forms as forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, USER_TYPES


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


class CreateCustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["user_type", "email", "password1", "password2", "full_name", "phone_number", "address", ]


class ViewUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["user_type", "email", "full_name", "phone_number", "address", ]
    user_type = forms.ChoiceField(choices=USER_TYPES, disabled=True)
    email = forms.EmailField(label="Email address", disabled=True)
    full_name = forms.CharField(disabled=True)
    phone_number = forms.CharField(disabled=True)
    address = forms.CharField(disabled=True)
