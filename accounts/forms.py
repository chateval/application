from django import forms

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    institution = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class' : 'input'}))

class LogInForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class' : 'input'}))