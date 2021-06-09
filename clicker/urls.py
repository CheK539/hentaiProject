from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'clicker'
urlpatterns = [
    path('saveCoins/', login_required(views.saveCoins), name='saveClick'),
    path('buyBoost/', login_required(views.buyBoost), name='buyBoostPage'),
]
