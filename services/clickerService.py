from hentai_information.models import GameModel, Boost, BoostDefault
from hentai_information.serializer import BoostSerializer, GameSerializer


def getGameModel(request):
    return GameModel.objects.filter(user=request.user.id).first()


def saveCoins(request):
    game_model = getGameModel(request)
    new_coins = request.data['coins']
    game_model.saveCoins(new_coins)


def getNewBoost(request):
    game_model = getGameModel(request)
    boost = None

    if game_model.checkGoal():
        game_model.nextGoal *= 7
        boost = showNextBoost(game_model, request.user)
        boost = BoostSerializer(boost).data
        game_model.save()

    return boost


def buyBoost(request):
    game_model = getGameModel(request)
    boost_id = request.data['boost_id']
    game_model.buyBoost(boost_id)

    boost = game_model.boosts.filter(id=boost_id).first()
    context = GameSerializer(game_model).data
    context['price'] = boost.price
    context['type'] = boost.type

    return context


def showNextBoost(game_model, user):
    last_boost = game_model.boosts.last()
    default_last_boost = BoostDefault.objects.filter(name=last_boost.name, power=last_boost.power).first()

    types = 2
    new_default_boost, is_new = BoostDefault.objects.get_or_create(id=default_last_boost.id + 1,
                                                                   type=(default_last_boost.type + 1) % types)

    if is_new:
        createNewDefaultBoost(default_last_boost, new_default_boost)

    new_boost = createNewBoost(new_default_boost, user)
    game_model.boosts.add(new_boost)

    return new_boost


def createNewDefaultBoost(default_last_boost, new_default_boost):
    number = len(BoostDefault.objects.filter(type=new_default_boost.type))

    if new_default_boost.type == 0:
        new_default_boost.name = f'Simp {number}'

    if new_default_boost.type == 1:
        new_default_boost.name = f'Auto click {number}'

    new_default_boost.price = default_last_boost.price * 11
    new_default_boost.power = default_last_boost.power * 5
    new_default_boost.save()


def createNewBoost(default_boost, user):
    new_boost = Boost()
    new_boost.user = user
    new_boost.name = default_boost.name
    new_boost.price = default_boost.price
    new_boost.power = default_boost.power
    new_boost.type = default_boost.type

    new_boost.save()

    return new_boost
