from django.shortcuts import render, redirect
from orm.models import Author, Model

def archive_model(request):
    model = Model.objects.get(pk=request.GET.get('model_id'))
    if request.user == model.author.author_id:
        model.archived = True
        model.save()
    return redirect('/uploads')