from django.db import models

class Images(models.Model):
    image = models.ImageField()
    updated = models.DateTimeField(auto_now=True)