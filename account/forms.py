from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from account import models as account_models


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = account_models.UserRegistration
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


# class UserUpdateForm(forms.ModelForm):

#     class Meta:
#         model = account_models.UserRegistration
#         fields = [
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#         ]


class ProfileUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        label="Email Address",
        disabled=True,
    )

    class Meta:
        model = account_models.UserRegistration
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'city',
            'zip_code',
            'image',
        ]


class CustomPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(
        label="Enter your email address",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        required=False,
    )
