# Generated by Django 5.1.3 on 2024-11-08 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="rating",
            field=models.IntegerField(
                blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True
            ),
        ),
    ]
