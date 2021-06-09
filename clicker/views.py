from rest_framework.decorators import api_view
from rest_framework.response import Response
from hentai_information.models import GameModel, BoostDefault, Boost
from hentai_information.serializer import BoostSerializer, GameSerializer


# Create your views here.

# ToDo:
#  1. Добавить задние фоны для страницы, улучшение внешнего вида

@api_view(['POST'])
def saveCoins(request):
    game_model = GameModel.objects.filter(user=request.user.id).first()
    new_coins = request.data['coins']

    game_model.saveCoins(new_coins)

    boost = None

    if game_model.checkGoal():
        game_model.nextGoal *= 7
        boost = showNextBoost(game_model, request.user)
        boost = BoostSerializer(boost).data
        game_model.save()

    content = {'boost': boost}
    return Response(content)


def showNextBoost(game_model, user):
    new_boost = game_model.boosts.last()
    default_boost = BoostDefault.objects.filter(name=new_boost.name, power=new_boost.power).first()

    types = 2
    new_default_boost, is_new = BoostDefault.objects.get_or_create(id=default_boost.id + 1,
                                                                   type=(default_boost.type + 1) % types)

    if is_new:
        number = len(BoostDefault.objects.filter(type=new_default_boost.type))

        if new_default_boost.type == 0:
            new_default_boost.name = f'Simp {number}'

        if new_default_boost.type == 1:
            new_default_boost.name = f'Auto click {number}'

        new_default_boost.price = default_boost.price * 11
        new_default_boost.power = default_boost.power * 5
        new_default_boost.save()

    new_boost = Boost()
    new_boost.user = user
    new_boost.name = new_default_boost.name
    new_boost.price = new_default_boost.price
    new_boost.power = new_default_boost.power
    new_boost.type = new_default_boost.type

    new_boost.save()

    game_model.boosts.add(new_boost)

    return new_boost


@api_view(['POST'])
def buyBoost(request):
    game_model = GameModel.objects.filter(user=request.user.id).first()
    boost_id = request.data['boost_id']
    game_model.buyBoost(boost_id)
    game_model.save()
    boost = game_model.boosts.filter(id=boost_id).first()

    context = GameSerializer(game_model).data
    context['price'] = boost.price
    context['type'] = boost.type

    return Response(context)
