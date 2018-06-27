from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from orm.models import Author
from .forms import LogInForm, SignUpForm

def login_view(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            return redirect('/accounts/login')
    form = LogInForm()
    return render(request, 'registration/login.html', {'form' : form})

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                 email=form.cleaned_data['email'],
                                 password=form.cleaned_data['password'],
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])
            author = Author(author_id=user,
                            name=form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'], 
                            institution=form.cleaned_data['institution'],
                            email=form.cleaned_data['email'])
            author.save()
            return redirect('/accounts/login')            
    form = SignUpForm()
    return render(request, 'registration/signup.html', {'form' : form})