from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'hentai_information'
urlpatterns = [
    path('', views.HentaiListPage.as_view(), name='hentaiListPage'),
    path('addHentai/', login_required(views.AddHentaiPage.as_view()), name='addHentaiPage'),
    path('view/', login_required(views.HentaiInformationPage.as_view()), name='viewHentaiPage'),
    path('json/', views.JsonList.as_view(), name='jsonPage'),
    path('json/<str:title>/', views.CurrentJson.as_view(), name='currentJsonPage')
]
