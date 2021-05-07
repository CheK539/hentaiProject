from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'hentai_information'
urlpatterns = [
    path('', views.ClickerPage.as_view(), name='clickerPage'),
    path('json/', staff_member_required(views.UsersGameJson.as_view()), name='usersGameJson'),
    path('json/<int:id>/', staff_member_required(views.CurrentUserJson.as_view()), name='currentGameJsonPage'),
    path('registerGame/', login_required(views.RegisterGamePage.as_view()), name='registerGamePage')
]
