from django.shortcuts import render
from .models import Dataset, Baseline
from .generate_prompts import load_dataset
from .link_responses import load_responses

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
        #load_dataset("app/datasets/ncm.txt", "ncm", "ewgwG", "Wegwe", "wegweg")
        load_responses("app/datasets/ncmresponses.txt", "ncm")
    return render(request, 'submit.html', {})
    
