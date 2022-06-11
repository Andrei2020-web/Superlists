from django.urls import reverse
from django.db import models
from django.conf import settings


# Create your models here.
class List(models.Model):
    '''Список'''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                              on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='friends')

    def get_absolute_url(self):
        '''получить абсолютный url'''
        return reverse('view_list', args=[self.id])

    @property
    def name(self):
        return self.item_set.first()


class Item(models.Model):
    ''''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text
