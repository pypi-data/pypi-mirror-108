# Generated by Django 3.1.4 on 2021-04-30 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0008_auto_20210314_1840"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="evaluate_predictions_automatically",
            field=models.BooleanField(
                default=False,
                help_text="Retrieve and display predictions when loading a task",
                verbose_name="evaluate predictions automatically",
            ),
        ),
    ]
