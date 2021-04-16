from django.db import models


# Create your models here.

class Hentai(models.Model):
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description')

    class Meta:
        verbose_name = 'Hentai'
        verbose_name_plural = 'Hentai'

    def __str__(self):
        return self.title
