from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='shop', unique=True)
