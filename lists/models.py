from collections import defaultdict

from django.db import models

# Create your models here.
class List(models.Model):
    ''''Список'''
    pass


class Item(models.Model):
    ''''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
