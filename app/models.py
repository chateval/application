from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        db_table = 'Dataset'

class Baseline(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        db_table = 'Baseline'