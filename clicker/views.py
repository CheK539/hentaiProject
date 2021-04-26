from django.http import HttpResponse

# Create your views here.
from hentai_information.models import GameModel


class GameController:
    @staticmethod
    def click(request):
        game_model = GameModel.objects.filter(user=request.user.id)[0]
        game_model.click()
        game_model.save()
        return HttpResponse(game_model.coins)
