# Generated by Django 3.1.4 on 2021-03-22 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0002_auto_20210310_2044"),
        ("users", "0002_auto_20210308_1559"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="active_organization",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="active_users",
                to="organizations.organization",
            ),
        ),
    ]
