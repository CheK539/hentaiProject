from django.contrib import admin
from .models import GameModel, BoostDefault, Boost

# Register your models here.

admin.site.register(GameModel)
admin.site.register(BoostDefault)
admin.site.register(Boost)