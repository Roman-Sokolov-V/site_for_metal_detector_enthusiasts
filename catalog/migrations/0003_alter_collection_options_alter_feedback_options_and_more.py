# Generated by Django 5.1.3 on 2024-11-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_feedback_rating"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collection",
            options={
                "verbose_name": "Collection",
                "verbose_name_plural": "Collections",
            },
        ),
        migrations.AlterModelOptions(
            name="feedback",
            options={"verbose_name": "Feedback", "verbose_name_plural": "Feedbacks"},
        ),
        migrations.AlterModelOptions(
            name="finding",
            options={"verbose_name": "Finding", "verbose_name_plural": "Findings"},
        ),
        migrations.AlterModelOptions(
            name="image",
            options={"verbose_name": "Image", "verbose_name_plural": "Images"},
        ),
        migrations.AlterField(
            model_name="collection",
            name="findings",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="collections", to="catalog.finding"
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="name",
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="finding",
            name="rating",
            field=models.IntegerField(
                blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True
            ),
        ),
    ]