from django.shortcuts import render
from .models import Dataset, Baseline
from .generate_prompts import load_dataset

def splash(request):
    datasets = Dataset.objects.all()
    baselines = Baseline.objects.all()
    return render(request, 'splash.html', {'datasets': datasets, 'baselines': baselines})

def models(request):
    return render(request, 'models.html', {})

def conversations(request):
    return render(request, 'conversations.html', {})

def submit(request):
    if request.method == "POST":
        print("posted") 
        # load_dataset("app/datasets/ncm.txt", "NCM", "Neural Conversation Model", "lol", "lol")
    return render(request, 'submit.html', {})