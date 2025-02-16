# Generated by Django 4.2.16 on 2024-11-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tournaments", "0004_tournament_use_pools_alter_tournament_location"),
        ("users", "0003_competitor_profil_pic_competitor_tournament_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="competitor",
            name="nb_tournaments_won",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="competitor",
            name="ranking",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="competitor",
            name="tournament",
            field=models.ManyToManyField(
                blank=True, null=True, to="tournaments.tournament"
            ),
        ),
    ]
