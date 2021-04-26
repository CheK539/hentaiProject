from django.contrib.auth.models import User
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


class GameModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    clickPower = models.IntegerField(default=1)

    def click(self):
        self.coins += self.clickPower

    def clickPowerUp(self, coin):
        self.clickPower += coin

    def __str__(self):
        return f'{self.user}: {self.coins}'
