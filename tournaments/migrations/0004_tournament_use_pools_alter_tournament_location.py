# Generated by Django 4.2.16 on 2024-11-02 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tournaments", "0003_remove_tournament_ongoing_tournament_state_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournament",
            name="use_pools",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="tournament",
            name="location",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
