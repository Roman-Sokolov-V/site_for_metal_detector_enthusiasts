# Generated by Django 5.1.3 on 2024-11-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_collection_options_alter_feedback_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="findings",
            field=models.ManyToManyField(
                blank=True, related_name="collections", to="catalog.finding"
            ),
        ),
    ]