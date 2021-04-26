from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, RedirectView
from rest_framework import generics

from .forms import HentaiForm
from .models import Hentai, GameModel
from .serializer import GameSerializer


class UsersGameJson(generics.ListAPIView):
    serializer_class = GameSerializer
    queryset = GameModel.objects.all()


class CurrentUserJson(generics.ListAPIView):
    serializer_class = GameSerializer
    model = GameModel

    def get_queryset(self):
        return self.model.objects.filter(user=self.kwargs['id'])


class RegisterGamePage(RedirectView):
    url = reverse_lazy('hentai_information:clickerPage')

    def get_redirect_url(self, *args, **kwargs):
        if not GameModel.objects.filter(user=self.request.user.id):
            game = GameModel()
            game.user = self.request.user
            game.save()

        return super().get_redirect_url()


class ClickerPage(TemplateView):
    template_name = 'hentai_information/clicker_page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        return redirect('authentication:login')

    def get_context_data(self, **kwargs):
        game_model = GameModel.objects.filter(user=self.request.user.id)[0]
        serializer = GameSerializer(game_model)
        context = super().get_context_data(**kwargs)
        context.update(serializer.data)
        return context


class HentaiListPage(ListView):
    template_name = 'hentai_information/hentai_list_page.html'
    model = Hentai

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        return redirect('authentication:login')


class AddHentaiPage(CreateView):
    template_name = 'hentai_information/add_hentai_page.html'
    model = Hentai
    form_class = HentaiForm
    success_url = reverse_lazy('hentai_information:hentaiListPage')


class HentaiInformationPage(TemplateView):
    template_name = 'hentai_information/hentai_information.html'

    def get_context_data(self, **kwargs):
        title = 'title'
        hentai = None
        parameters = self.request.GET

        if title in parameters and parameters[title]:
            hentai = Hentai.objects.filter(title=parameters[title]).first()

        context = super().get_context_data(**kwargs)
        context['hentai'] = hentai
        return context
