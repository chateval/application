from django.db import models
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)

class Model(models.Model):
    author_id = models.ForeignKey('frontend.Author', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class SplashDataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class SplashBaseline(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()