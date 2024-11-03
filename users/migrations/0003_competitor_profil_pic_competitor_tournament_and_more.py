# Generated by Django 4.2.16 on 2024-11-02 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "tournaments",
            "0002_match_competitor_1_match_competitor_2_match_pool_and_more",
        ),
        ("users", "0002_fencer_discipline_referee_nb_tournaments_officiated_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="competitor",
            name="profil_pic",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="competitor",
            name="tournament",
            field=models.ManyToManyField(to="tournaments.tournament"),
        ),
        migrations.AddField(
            model_name="referee",
            name="profil_pic",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name="competitor",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="competitor",
            name="nb_tournaments_won",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="fencer",
            name="discipline",
            field=models.PositiveIntegerField(
                choices=[(1, "Epee"), (2, "Sabre"), (3, "Fleuret")],
                default=1,
                verbose_name="discipline",
            ),
        ),
        migrations.AlterField(
            model_name="referee",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
