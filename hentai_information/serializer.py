from rest_framework import serializers

from hentai_information.models import Hentai, GameModel


class HentaiListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hentai
        fields = ['title']


class HentaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hentai
        fields = ['title', 'description']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameModel
        fields = ['user', 'coins']
