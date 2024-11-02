from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import requests
from django.contrib.auth.forms import SetPasswordForm



class UserTypeForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['user_type']


class SchoolInfoForm(forms.ModelForm):
    country = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['country']

    def __init__(self, *args, **kwargs):
        super(SchoolInfoForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = self.get_country_choices()

    def get_country_choices(self):
        try:
            response = requests.get('https://restcountries.com/v3.1/all')
            countries = response.json()
            return [(country['name']['common'], country['name']['common']) for country in countries]
        except Exception:
            return []


class PersonalInfoForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    phone_number = forms.CharField(max_length=14, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone_number']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username


class AccountInfoForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'minlength': 8}), help_text="Password must be at least 8 characters long.")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'minlength': 8}), help_text="Enter the same password as before, for verification.")
    secret_code = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'secret_code']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use another email address.")
        return email


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

class PasswordResetForm(SetPasswordForm):
    pass  # You can customize it if you want

class PasswordResetVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter verification code'})
    )