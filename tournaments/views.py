from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib import messages
from .models import Tournament, Competitor, Participation, Match
from . import logger, MAX_COMPETITORS


def tournaments(request):
    tournaments = Tournament.objects.all().values()
    template = loader.get_template("tournaments.html")
    context = {
        "tournaments": tournaments,
    }
    return HttpResponse(template.render(context, request))


def generate_tournament(request):
    logger.info("generate_tournament init")
    competitors = Competitor.objects.all().values()

    # retrieve data from html form
    if request.method == "POST":
        logger.info("generate_tournament post")
        name = request.POST["name"]
        date = request.POST["date"]
        location = request.POST["location"]
        max_nb_participants = request.POST["max_nb_participants"]
        use_pools = "use_pools" in request.POST

        # retrieve the existing competitors
        existing_competitors_ids = request.POST.getlist("existing_competitors")
        # retrieve the new competitors
        new_competitor_last_name = [
            last_name
            for last_name in request.POST.getlist("new_competitor_last_name[]")
            if last_name
        ]
        new_competitor_first_name = [
            first_name
            for first_name in request.POST.getlist("new_competitor_first_name[]")
            if first_name
        ]
        new_competitor_ranking = [
            ranking
            for ranking in request.POST.getlist("new_competitor_ranking[]")
            if ranking
        ]
        logger.debug(
            "existing_competitors_ids=[{}]".format(
                ";".join(map(str, existing_competitors_ids))
            )
        )
        logger.debug(
            "new_competitor_first_name=[{}]".format(
                ";".join(map(str, new_competitor_first_name))
            )
        )

        # check nb participants
        nb_participants = len(existing_competitors_ids) + len(new_competitor_first_name)
        if not Tournament.check_nb_participants(nb_participants, MAX_COMPETITORS):
            logger.warn(
                "Generate Tournament - nb of participants incorrect. Please 3 <= nb_participants <= 32"
            )
            return render(
                request, "generate_tournament.html", {"competitors": competitors}
            )

        # create tournament object
        tournament = Tournament.objects.create(
            name=name,
            date=date,
            max_nb_participants=max_nb_participants,
            nb_participants=nb_participants,
            location=location,
            use_pools=use_pools,
        )

        all_competitors = []

        for competitor_id in existing_competitors_ids:
            competitor = Competitor.objects.get(id=competitor_id)
            all_competitors.append(competitor)
            Participation.objects.create(tournament=tournament, competitor=competitor)

        for i in range(len(new_competitor_first_name)):  # todo check same length
            if new_competitor_first_name[i]:  # make sure field not empty
                new_competitor = Competitor.objects.create(
                    last_name=new_competitor_last_name[i],
                    first_name=new_competitor_first_name[i],
                    ranking=new_competitor_ranking[i]
                    if new_competitor_ranking[i]
                    else 0,  # no magic nb to change to default value
                )
                all_competitors.append(new_competitor)
                Participation.objects.create(
                    tournament=tournament, competitor=new_competitor
                )
        logger.debug(f"tournament.nb_participants={tournament.nb_participants}")

        logger.debug("generates matches")
        # Generate matches between each pair of competitors
        list_matches = create_pairs(all_competitors)
        stage = Match.compute_stage(len(all_competitors))
        for match in list_matches:
            matches_as_competitor1 = match[0]
            if len(match) == 2:
                matches_as_competitor2 = match[1]
                Match.objects.create(
                    tournament=tournament,
                    competitor_1=matches_as_competitor1,
                    competitor_2=matches_as_competitor2,
                    stage=stage,
                )
            else:
                Match.objects.create(
                    tournament=tournament,
                    competitor_1=matches_as_competitor1,
                    stage=stage + 1,
                )

        logger.info("Tournament and matches successfully created")
        messages.success(request, "Tournament successfully created ")

        return redirect("tournaments")

    return render(request, "generate_tournament.html", {"competitors": competitors})


# TODO refactor
def create_pairs(lst):
    pairs = [(lst[i], lst[i + 1]) for i in range(0, len(lst) - 1, 2)]
    if len(lst) % 2 != 0:
        pairs.append((lst[-1],))  # Keep the last element as a single item
    return pairs


def tournament_details(request, id):
    try:
        tournament = Tournament.objects.get(id=id)
        participants = Participation.objects.filter(
            tournament=tournament
        ).select_related("competitor")

        # Fetch match related to this tournament, along with pools if any
        matches = Match.objects.filter(tournament=tournament)

        logger.debug(matches)
        logger.debug(matches[0].stage)
        logger.debug(type(matches[0].stage))

        context = {
            "tournament": tournament,
            "participants": participants,
            "matches": matches,
            "test": Match.objects.first(),
        }
    except Tournament.DoesNotExist:
        raise Http404("Tournament does not exist")

    return render(request, "tournament_details.html", context)
