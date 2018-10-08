from django import forms

class UploadModelForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    description = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    repo_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    checkpoint_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    institution = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class LogInForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))