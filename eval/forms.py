from django import forms
from django.utils.safestring import mark_safe

class ReadOnlyText(forms.TextInput):
  input_type = 'text'

  def render(self, name, value, attrs=None):
     if value is None: 
         value = ''
     return value

class UploadModelForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Name</b><br/>Give a human-readable name for your system.'))
    description = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Description</b><br/>This field should includes things like a '
                                           'description of the architecture you trained with, the strategy '
                                           'that was used to decode samples, the training data, or a link to your paper.'))
    repo_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Code Respository</b><br/>If your code is open-source, where '
                                           'can it be found?'))
    checkpoint_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Model weights</b><br/>If you have made your model weights public, give '
                                           ' a download link.'))

class DBDC5Form(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Name</b><br/>Give a human-readable name for your system.'))
    submission_info = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Submission Number</b>'))
    submission_track = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Submission Track</b>'))

class DSTC10Form(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Name</b><br/>Give a human-readable name for your submission.'))
    submission_info = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Submission Number</b>'))
    submission_track = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Submission Track</b>'))

class DSTC11Form(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Name</b><br/>Give a human-readable name for your submission.'))
    submission_info = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Submission Number</b>'))
    submission_track = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Submission Track</b>'))

class GEMV3Form(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Team Name</b><br/>Team name for your submission.'))
    email = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
                           label=mark_safe('<b>Email</b><br/>Primary email for your submission.'))
    TASK_CHOICES = [
        ('D2T-1', 'D2T-1 (3 files expected per language)'),
        ('D2T-2', 'D2T-2 (3 files expected per language)'),
        ('Summ-1', 'Summ-1'),
        ('Summ-2', 'Summ-2'),
        ('Summ-3', 'Summ-3'),
    ]
    # submission_track = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}),
    #                       label=mark_safe('<b>Submission Track</b>'))
    submission_track = forms.MultipleChoiceField(
        choices=TASK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label=mark_safe('<b>Submission Track</b>'),
    )


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
