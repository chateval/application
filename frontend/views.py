from django.shortcuts import render
from .models import Model, SplashDataset, SplashBaseline
from .forms import ModelForm

def splash(request):
    datasets = SplashDataset.objects.all()
    baselines = SplashBaseline.objects.all()
    return render(request, 'splash.html', {'datasets': datasets, 'baselines': baselines})

def models(request):
    return render(request, 'models.html', {})

def conversations(request):
    return render(request, 'conversations.html', {})

def submit(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            return redirect('splash')
    else:      
        form = ModelForm()
        return render(request, 'submit.html', {'form': form})