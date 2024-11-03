from django.db import models
from django.urls import reverse
from users.models import Competitor
from django.utils.translation import gettext_lazy as _  # for label


class Tournament(models.Model):
    """Tournament model described with an optionnal pool phase and stages
    Parameters
    ----------
    int - id: tournament's id
    str - name: Name of the tournament
    date - date: starting date of the tournament
    str - state: state of the tournament
    str - location: location of the tournament
    int - max_nb_participants: max number participants in the tournament
    int - nb_participants: number participants in the tournament
    str - winner: winner of the tournament
    bool - use_pool: defines if the tournament has a pool phase
    """

    class State(models.TextChoices):
        FUN = "FUN"  # tournament for fun - not official
        REGISTRATION = "REG"
        STARTED = "STA"
        FINISHED = "END"

    id: int = models.AutoField(primary_key=True)
    name: str = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    state: str = models.CharField(
        max_length=3, choices=State.choices, default=State.FUN
    )
    location: str = models.CharField(max_length=50, blank=True, null=True)
    max_nb_participants: int = models.PositiveIntegerField()
    nb_participants: int = models.PositiveIntegerField(default=3)
    winner: str = models.CharField(max_length=50, blank=True, null=True)
    use_pools: bool = models.BooleanField(default=False)

    @staticmethod
    def check_nb_participants(nb_participants, max_competitors):
        return nb_participants <= max_competitors and 2 < nb_participants

    def get_absolute_url(self):
        return reverse("tournament_details", args=[str(self.id)])

    def __str__(self):
        return f"Tournament {self.name}"

    # TODO if nb players > 32 => pool automatically : can be disabled but true by default


class Pool(models.Model):
    max_competitors: int = models.PositiveIntegerField(default=3)
    tournament_name: str = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, blank=True, null=True
    )

    def add_competitor(
        self,
    ):
        # TODO
        pass

    def __str__(self):
        return f"Tournament {self.name}"


class Match(models.Model):
    class Stages(models.IntegerChoices):
        POOL = 0, _("Pool")
        round_of_32 = 1, _("Round of 32")
        round_of_16 = 2, _("Round of 16")
        round_of_8 = 3, _("Round of 8")
        round_of_4 = 4, _("Round of 4")
        final = 5, _("Final")

    def increment_stage(self):
        max_stages = max(stage.value for stage in Match.Stages)
        self.stage = int(
            self.stage
        )  # TODO check why innerclass Stages is not an integer
        if self.stage < max_stages:
            self.stage += 1
            self.save()

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="matches",
        blank=True,
        null=True,
    )
    stage: int = models.IntegerField(choices=Stages.choices, default=Stages.POOL)
    pool = models.ForeignKey(
        Pool, on_delete=models.CASCADE, related_name="matches", blank=True, null=True
    )
    competitor_1 = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name="matches_as_competitor1",
        blank=True,
        null=True,
    )
    competitor_2 = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name="matches_as_competitor2",
        blank=True,
        null=True,
    )
    winner: str = models.CharField(max_length=50, null=True)
    score: str = models.CharField(max_length=50, null=True)

    def update_winner():
        # TODO
        pass

    @classmethod
    def compute_stage(cls, nb_participants):
        stage = cls.Stages.POOL  # default
        if nb_participants < 3:  # TODO remove magic number
            stage = cls.Stages.final
        elif nb_participants < 5:
            stage = cls.Stages.round_of_4
        elif nb_participants < 9:
            stage = cls.Stages.round_of_8
        elif nb_participants < 17:
            stage = cls.Stages.round_of_16
        elif nb_participants < 33:
            stage = cls.Stages.round_of_32
        return stage

    class Meta:
        """Ensures a match belongs to only one tournament"""

        unique_together = ("tournament", "competitor_1", "competitor_2")

    def __str__(self):
        return f"Tournament {self.tournament.name} Stage {self.stage} - Match {self.competitor_1.first_name} vs {self.competitor_2.first_name}"


class Participation(models.Model):
    """Participation: keep track of participation of a competitor in a tournament.
    Parameters
    ----------
    int - tournament: User's id
    str - competitor: Name of the tournament
    date - registration_date: registration date to the tournament
    str - state: state of the tournament
    """

    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="participants"
    )
    competitor = models.ForeignKey(
        Competitor, on_delete=models.CASCADE, related_name="tournaments"
    )
    registration_date = models.DateField(auto_now_add=True)
    pool = models.ForeignKey(
        Pool,
        on_delete=models.SET_NULL,
        related_name="competitors",
        blank=True,
        null=True,
    )

    class Meta:
        """Ensures a competitor participates only once in a tournament"""

        unique_together = ("tournament", "competitor")

    def __str__(self):
        return f"{self.competitor.first_name} in {self.tournament.name}"
