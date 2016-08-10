from django.db import models


class FlatPage(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
