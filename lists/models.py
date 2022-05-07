from django.urls import reverse
from django.db import models


# Create your models here.
class List(models.Model):
    ''''Список'''

    def get_absolute_url(self):
        '''получить абсолютный url'''
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    ''''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
