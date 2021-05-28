from rest_framework import serializers

from hentai_information.models import GameModel, Boost


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameModel
        fields = ['user', 'coins', 'clickPower']


class BoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boost
        fields = ['id', 'power', 'price', 'name']
