# Generated by Django 4.2.16 on 2024-11-03 08:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tournaments", "0007_rename_nb_participants_tournament_max_nb_participants"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournament",
            name="nb_participants",
            field=models.PositiveIntegerField(default=3),
        ),
    ]
