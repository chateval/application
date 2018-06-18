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
<<<<<<< HEAD
        print(request.POST.get('model_url'))    
    return render(request, 'submit.html', {})
    
=======
        print("posted") 
        # load_dataset("app/datasets/ncm.txt", "NCM", "Neural Conversation Model", "lol", "lol")
    return render(request, 'submit.html', {})
>>>>>>> 4f20223809eaff16d81ad49a77be53f63bf1f525
