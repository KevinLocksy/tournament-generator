# Generated by Django 4.2.16 on 2024-11-02 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Competitor",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("ranking", models.IntegerField()),
                ("nb_tournaments_participated", models.IntegerField()),
                ("nb_tournaments_won", models.IntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Referee",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Fencer",
            fields=[
                (
                    "competitor_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="users.competitor",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("users.competitor",),
        ),
    ]
