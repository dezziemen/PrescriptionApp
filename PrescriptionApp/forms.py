import django.forms as forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Accounts.models import CustomUser
from Accounts.models import USER_TYPES


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
