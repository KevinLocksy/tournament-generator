from django.db import models


class User(models.Model):
    """abstract class: define User structure
    Parameters
    ----------
    int - id: User's id
    str - first_name: User's first name
    str - last_name: User's last name
    str - profil_pic: User's profil picture's path
    """

    id: int = models.AutoField(primary_key=True)
    first_name: str = models.CharField(max_length=50)
    last_name: str = models.CharField(max_length=50)
    profil_pic: str = models.CharField(
        max_length=5000, blank=True, null=True
    )  # TODO check max_length

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.last_name = self.last_name.upper()
        super(User, self).save(force_insert, force_update, *args, **kwargs)

    @property
    def full_name(self):
        "Returns the person's full name."
        return f"{self.first_name.capitalize()} {self.last_name.upper()}"

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"


class Competitor(User):
    """extends User class
    Parameters
    ----------
    link - tournament: many to many
    int - ranking: User's ranking
    int - nb_tournaments_participated: number of tournaments participated by the user
    int - nb_tournaments_won: number of tournaments won by the user
    """

    tournament = models.ManyToManyField(
        to="tournaments.Tournament", blank=True, null=True
    )
    ranking: int = models.PositiveIntegerField(default=0)  # 0 = fun
    nb_tournaments_participated: int = models.PositiveIntegerField(default=0)
    nb_tournaments_won: int = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name.upper()} - ranked {self.ranking}"


class Fencer(Competitor):
    """
    Extends Competitor to add a fencing discipline
    Parameters
    ----------
    int - discipline: fencing discipline
    """

    class Discipline(models.IntegerChoices):
        EPEE = 1, "Epee"
        SABRE = 2, "Sabre"
        FLEURET = 3, "Fleuret"

    discipline: int = models.PositiveIntegerField(
        choices=Discipline.choices, default=Discipline.EPEE, verbose_name="discipline"
    )
    club: str = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name.upper()}: {self.discipline} - ranked {self.ranking}"


class Referee(User):
    """Only for official tournaments - defines official referees
    Extends User class
    Parameters
    ----------
    int - nb_tournaments_officiated: number of tournaments officiated by the referee
    """

    nb_tournaments_officiated: int = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Referee - {self.first_name} {self.last_name.upper()}"
