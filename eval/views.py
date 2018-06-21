from django.shortcuts import render
from core.models import Author, Model

def my_models(request):
    current_author = Author.objects.get(author_id=request.user)
    models = Model.objects.filter(author=current_author)
    return render(request, 'my_models.html', {'models': models})