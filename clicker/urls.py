from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'clicker'
urlpatterns = [
    path('click/', login_required(views.click), name='clickPage'),
    path('buyBoost/', login_required(views.buyBoost), name='buyBoostPage'),
]
