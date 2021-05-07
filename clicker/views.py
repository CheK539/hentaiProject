import json

from django.http import HttpResponse

# Create your views here.
from hentai_information.models import GameModel


def click(request):
    game_model = GameModel.objects.filter(user=request.user.id).first()
    game_model.click()
    game_model.save()
    return HttpResponse(game_model.coins)


def buyBoost(request, **kwargs):
    game_model = GameModel.objects.filter(user=request.user.id).first()
    boost_id = kwargs['id']
    game_model.buyBoost(boost_id)
    game_model.save()
    boost = game_model.boosts.filter(id=boost_id).first()
    content = {'clickPower': game_model.clickPower, 'coins': game_model.coins, 'price': boost.price}
    return HttpResponse(json.dumps(content))
