from django.contrib import admin
from .models import Tournament, Match, Pool, Participation

admin.site.register(Participation)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(Pool)
