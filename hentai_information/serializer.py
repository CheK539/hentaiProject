from rest_framework import serializers

from hentai_information.models import GameModel


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameModel
        fields = ['user', 'coins', 'clickPower']
