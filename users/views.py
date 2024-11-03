from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template import loader
from .models import Competitor, Referee
from tournaments.models import Participation


def users(request):
    competitors = Competitor.objects.all().values()
    template = loader.get_template("users.html")
    context = {
        "competitors": competitors,
    }
    return HttpResponse(template.render(context, request))


def referees(request):
    referees = Referee.objects.all().values()
    template = loader.get_template("referees.html")
    context = {
        "referees": referees,
    }
    return HttpResponse(template.render(context, request))


def user_details(request, id):
    try:
        competitor = Competitor.objects.get(id=id)
        tournaments = Participation.objects.filter(
            competitor=competitor
        ).select_related("tournament")
        context = {
            "competitor": competitor,
            "tournaments": tournaments,
        }
    except Competitor.DoesNotExist:
        raise Http404("Tournament does not exist")

    return render(request, "user_details.html", context)


def generate_user(request):
    if request.method == "POST":
        m_firstname = request.POST["first_name"]
        m_lastname = request.POST["last_name"]
        m_is_referee = request.POST["is_referee"]
        if m_is_referee:
            referee = Referee(first_name=m_firstname, last_name=m_lastname)
            referee.save()
        else:
            m_ranking = request.POST["ranking"]
            competitor = Competitor(
                first_name=m_firstname, last_name=m_lastname, ranking=m_ranking
            )
            competitor.save()
        return HttpResponseRedirect(reverse("home"))
    return render(
        request,
        "generate_user.html",
    )
