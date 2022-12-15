from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from datetime import date
from django.core.exceptions import ValidationError


today = date.today()

class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists!")
        return email


