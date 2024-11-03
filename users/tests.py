from django.test import TestCase
from django.urls import reverse
from .models import Competitor


class UsersTests(TestCase):
    def setUp(self):
        self.competitor = Competitor.objects.create(
            first_name="John",
            last_name="Smith",
            profil_pic="path_img",
            ranking=1,
            nb_tournaments_participated=2,
            nb_tournaments_won=1,
        )

    def test_competitor_creation(self):
        """Test competitor creation and field values"""
        self.assertEqual(self.competitor.first_name, "John")
        self.assertEqual(self.competitor.last_name, "SMITH")
        self.assertEqual(self.competitor.ranking, 1)
        self.assertEqual(self.competitor.nb_tournaments_participated, 2)
        self.assertEqual(self.competitor.nb_tournaments_won, 1)

    def test_competitor_detail_view(self):
        """Test competitor detail view returns the correct data"""
        url = reverse("user_details", args=[self.competitor.id])
        response = self.client.get(url)

        # is response successful
        self.assertEqual(response.status_code, 200)

        # is competitor data in context
        self.assertEqual(response.context["competitor"].first_name, "John")
