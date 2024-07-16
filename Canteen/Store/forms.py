from django import forms
from django.contrib.auth.models import User
import re


class LoginForm(forms.Form):
    username = forms.CharField(label="e-mail", required=True, widget=forms.TextInput(attrs={'class':' grow text-info', 'placeholder':'e.g. someone@email.com'}))
    password = forms.CharField(label="Password",required=True, widget=forms.PasswordInput(attrs={'class':' grow text-info', 'placeholder':'password'}))


class RegisterForm(forms.Form):
    name = forms.CharField(label="Name", required=True,widget=forms.TextInput(attrs={'class':' grow text-info', 'placeholder':'e.g. Ram'}))
    email = forms.CharField(label="e-Mail",required=True,widget=forms.EmailInput(attrs={'class':' grow text-info', 'placeholder':'e.g. someone@email.com'}) )
    phone = forms.CharField(label="Phone", required=True, widget=forms.TextInput(attrs={'class':' grow text-info', 'placeholder':'8787878787 '}))
    address = forms.CharField(label="Address", required=True,widget=forms.TextInput(attrs={'class':' grow text-info', 'placeholder':'NBH C block'}))
    password = forms.CharField(label="Password",required=True,widget=forms.PasswordInput(attrs={'class':' grow text-info', 'placeholder':'password'}))
    # retype_password = forms.CharField(label="Retype Password",required=True, widget=forms.PasswordInput)


    def clean_email(self):
        pattern = r'^[a-zA-Z0-9._%+-]+@bbdu\.ac\.in$'

        data = self.cleaned_data["email"]
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("Email already registered!")
        
        if not re.match(pattern, data):
            raise forms.ValidationError("enter your official email ending with -@bbdu.ac.in")
        return data

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6:
            raise forms.ValidationError("length of password is less than 6")
        else:
            return password
        

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        if len(data) != 10 or data.isdigit() != True:
            raise forms.ValidationError("Invalid mobile no.")
        else:
            return data

class UserEditForm(forms.Form):
    name = forms.CharField(label="Full Name", required=True, widget=forms.TextInput(attrs={'class':' grow'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'readonly': 'readonly','class':'grow'}))
    phone = forms.CharField(label="Phone no", required=True, widget=forms.TextInput(attrs={'class':' grow'}))
    address = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class':' grow'}), required=True)

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        if len(data) != 10 or data.isdigit() != True:
            raise forms.ValidationError("Invalid mobile no.")
        else:
            return data