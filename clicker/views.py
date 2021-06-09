from rest_framework.decorators import api_view
from rest_framework.response import Response
from services import clickerService


# Create your views here.


@api_view(['POST'])
def saveCoins(request):
    clickerService.saveCoins(request)
    boost = clickerService.getNewBoost(request)
    content = {'boost': boost}

    return Response(content)


@api_view(['POST'])
def buyBoost(request):
    context = clickerService.buyBoost(request)

    return Response(context)
