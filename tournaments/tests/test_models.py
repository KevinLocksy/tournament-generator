from django.test import TestCase
from django.urls import reverse
from ..models import Tournament, Match
from users.models import Competitor


class TournamentTests(TestCase):
    def setup(self):
        self.tournament = Tournament.objects.create(
            name="Tournament_Name",
            state=Tournament.State.FUN,
            location="World",
            max_nb_participants=32,
            use_pools=False,
        )

    def test_create_tournament_from_page_fail_not_enough_participants(self):
        data_fail_not_enough_participants = {
            "name": "testTournamentName",
            "state": Tournament.State.FUN,
            "date": "2000-01-01",
            "location": "world",
            "max_nb_participants": 32,
            "use_pools": False,
            "existing_competitors": [1, 2],
        }
        response = self.client.post(
            reverse("generate_tournaments"), data_fail_not_enough_participants
        )
        self.assertEqual(response.status_code, 200)

    # TODO use mock
    def create_tournament(self):
        competitor_1 = Competitor.objects.create(
            first_name="John",
            last_name="Smith",
            profil_pic="path_img",
            ranking=1,
            nb_tournaments_participated=2,
            nb_tournaments_won=1,
        )
        competitor_2 = Competitor.objects.create(
            first_name="John_2",
            last_name="Smith",
            profil_pic="path_img",
            ranking=2,
            nb_tournaments_participated=2,
            nb_tournaments_won=1,
        )
        competitor_3 = Competitor.objects.create(
            first_name="John_3",
            last_name="Smith",
            profil_pic="path_img",
            ranking=3,
            nb_tournaments_participated=2,
            nb_tournaments_won=1,
        )
        competitor_4 = Competitor.objects.create(
            first_name="John_4",
            last_name="Smith",
            profil_pic="path_img",
            ranking=4,
            nb_tournaments_participated=2,
            nb_tournaments_won=1,
        )
        data_enough_participants = {
            "name": "testTournamentName",
            "state": Tournament.State.FUN,
            "date": "2000-01-01",
            "location": "world",
            "max_nb_participants": 32,
            "use_pools": False,
            "existing_competitors": [1, 2, 3, 4],
        }
        return self.client.post(
            reverse("generate_tournaments"), data_enough_participants
        )

    # @patch('users.models.Competitor')
    def test_create_tournament_matches_from_page_success(self):
        # all_competitors = [MagicMock(id=i) for i in range(4)]
        # MockCompetitor.objects.all.return_value = all_competitors

        response = self.create_tournament()
        self.assertEqual(response.status_code, 302)
        matches = Match.objects.all()
        self.assertEqual(matches.count(), 2)

    def test_correct_pairs_opponents_match(self):
        response = self.create_tournament()
        self.assertEqual(response.status_code, 302)
        matches = Match.objects.all()
        self.assertEqual(matches[0].competitor_1.first_name, "John")
        self.assertEqual(matches[0].competitor_2.first_name, "John_2")
        self.assertEqual(matches[1].competitor_1.first_name, "John_3")
        self.assertEqual(matches[1].competitor_2.first_name, "John_4")

    def test_increment_stage(self):
        matches = Match.objects.all()
        self.assertEqual(int(matches[0].stage), 4)
        matches[0].increment_stage()
        self.assertEqual(int(matches[0].stage), 5)
