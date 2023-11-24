from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.ModelForm):
    ROLE_CHOICES = (
    ('Buyer','Buyer'),
    ('Seller','Seller'),
    )
    username = forms.CharField(label='Enter Username',min_length=4,max_length=50,help_text='*Required')
    email = forms.EmailField(max_length=100,help_text='*Required',error_messages={'required':'Please enter your email'})
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=10,min_length=10)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = UserBase
        fields = ('username','email','phone_number','role')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
