from django.shortcuts import render
from users.models import Competitor
from tournaments.models import Tournament
from . import LIMIT_QUERY


def home(request):
    competitors = Competitor.objects.all().values().order_by("-id")[:LIMIT_QUERY]
    tournaments = Tournament.objects.all().values().order_by("-id")[:LIMIT_QUERY]
    context = {
        "competitors": competitors,
        "tournaments": tournaments,
    }
    return render(request, "home.html", context)
