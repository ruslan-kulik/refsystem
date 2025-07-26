from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
        required=True,
    )
    phone_number = forms.CharField(
        label=_("Phone Number"),
        max_length=15,
        widget=forms.TextInput(attrs={"autocomplete": "tel"}),
        required=True,
    )
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        required=False,
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    invite_code_input = forms.CharField(
        label=_("Invite Code"),
        max_length=6,
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "off", "placeholder": "Если есть"})
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "invite_code_input",
        )


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        required=True,
    )
    phone_number = forms.CharField(
        label=_("Phone Number"),
        max_length=15,
        required=True,
    )
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        required=False,
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "email",
            "first_name",
            "last_name",
        )


class ActivateInviteForm(forms.Form):
    invite_code = forms.CharField(
        label=_("Invite Code"),
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Введите код"})
    )
