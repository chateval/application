from django import forms

class UploadModelForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'input'}))
    description = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'input'}))
    repo_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'input'}))
    checkpoint_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'input'}))