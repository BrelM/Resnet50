from django.db import models

class Images(models.Model):
    image = models.ImageField()
    updated = models.DateTimeField(auto_now=True)


class Nom(models.Model):
    nom = models.CharField(max_length=255)
    a_vote = models.BooleanField(default=False)
    char = models.CharField(max_length=int(1e10), blank=True)