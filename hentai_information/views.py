from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from rest_framework import generics

from .models import GameModel, BoostDefault, Boost
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
            for boost_base in BoostDefault.objects.all():
                boost = Boost()

                boost.user = self.request.user
                boost.name = boost_base.name
                boost.price = boost_base.price
                boost.power = boost_base.power

                boost.save()
                game.boosts.add(boost)

        return super().get_redirect_url()


class ClickerPage(TemplateView):
    template_name = 'hentai_information/clicker_page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        return redirect('authentication:login')

    def get_context_data(self, **kwargs):
        game_model = GameModel.objects.filter(user=self.request.user.id).first()
        serializer = GameSerializer(game_model)
        context = super().get_context_data(**kwargs)
        context.update(serializer.data)
        context['boosts'] = game_model.boosts.all()
        return context
