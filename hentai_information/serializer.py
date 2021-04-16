from rest_framework import serializers

from hentai_information.models import Hentai


class HentaiListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hentai
        fields = ['title']


class HentaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hentai
        fields = ['title', 'description']
