from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hentai_information.models import GameModel, BoostDefault, Boost
from hentai_information.serializer import BoostSerializer


# Create your views here.

@api_view(['GET'])
def click(request):
    game_model = GameModel.objects.filter(user=request.user.id).first()
    boost = None

    if game_model.checkGoal():
        game_model.nextGoal *= 7
        boost = showNextBoost(game_model, request.user)
        boost = BoostSerializer(boost).data

    game_model.click()

    content = {'coins': game_model.coins, 'boost': boost}
    return Response(content)


def showNextBoost(game_model, user):
    new_boost = game_model.boosts.last()
    default_boost = BoostDefault.objects.filter(name=new_boost.name, power=new_boost.power).first()

    new_default_boost, is_new = BoostDefault.objects.get_or_create(id=default_boost.id + 1)

    if is_new:
        new_default_boost.name = f'Simp {len(BoostDefault.objects.all())}'
        new_default_boost.price = default_boost.price * 11
        new_default_boost.power = default_boost.power * 5
        new_default_boost.save()

    new_boost = Boost()

    new_boost.user = user
    new_boost.name = new_default_boost.name
    new_boost.price = new_default_boost.price
    new_boost.power = new_default_boost.power

    new_boost.save()

    game_model.boosts.add(new_boost)

    return new_boost


@api_view(['POST'])
def buyBoost(request):
    if request.method == 'POST':
        game_model = GameModel.objects.filter(user=request.user.id).first()

        boost_id = request.data['boost_id']
        game_model.buyBoost(boost_id)
        game_model.save()
        boost = game_model.boosts.filter(id=boost_id).first()
        content = {'clickPower': game_model.clickPower, 'coins': game_model.coins, 'price': boost.price}

        # return HttpResponse(json.dumps(content))
        return Response(content)

    raise Http404()
