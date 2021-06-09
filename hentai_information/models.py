from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class BoostBase(models.Model):
    name = models.CharField(max_length=50)
    power = models.IntegerField(default=1)
    price = models.IntegerField(default=10)
    type = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True


class BoostDefault(BoostBase):
    def __str__(self):
        return f'{self.name}: {self.power}'


class Boost(BoostBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}: {self.user}'


class GameModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    clickPower = models.IntegerField(default=1)
    autoClickPower = models.IntegerField(default=0)
    boosts = models.ManyToManyField(Boost)
    nextGoal = models.IntegerField(default=20)

    def saveCoins(self, new_coins):
        self.coins = new_coins
        self.save()

    def checkGoal(self):
        return self.coins > self.nextGoal

    def buyBoost(self, boost_id):
        boost = self.boosts.filter(id=boost_id).first()

        if boost.price > self.coins:
            return

        if boost.type == 0:
            self.clickPower += boost.power

        if boost.type == 1:
            self.autoClickPower += boost.power

        self.coins -= boost.price
        boost.price = int(boost.price * 1.5 + 0.5)

        boost.save()
        self.save()

    def __str__(self):
        return f'{self.user}: {self.coins}'
