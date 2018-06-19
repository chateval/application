from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    institution = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    confirm_password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))

class LogInForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))

class UploadModelForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    description = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    repo_location = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    cp_location = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    response_dataset = forms.FileField()