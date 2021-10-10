import django.forms as forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Accounts.models import CustomUser


class CreateCustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["user_type", "email", "password1", "password2", "full_name", "phone_number", "address", ]

