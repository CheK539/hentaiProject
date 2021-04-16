from django import forms

from .models import Hentai


class HentaiForm(forms.ModelForm):
    class Meta:
        model = Hentai
        fields = ('title', 'description')
