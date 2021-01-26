from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account import models as account_models
from account import forms as account_forms


class UserRegistrationAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_superuser',)
    list_filter = ('is_superuser',)
    model = account_models.UserRegistration
    add_form = account_forms.UserRegistrationForm
    fieldsets = (
        (('Personal info'), {'fields': ('username', 'password', 'first_name',
                                        'last_name', 'email', 'image', 'city',
                                        'phone_number', 'address', 'zip_code',)}),

        (('Permissions'), {'fields': ('is_superuser', 'is_active')}),

        (('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name',
                       'email', 'password1', 'password2', 'phone_number',
                       'is_superuser', 'is_active',)
        }
        ),
    )


admin.site.register(account_models.UserRegistration, UserRegistrationAdmin)
