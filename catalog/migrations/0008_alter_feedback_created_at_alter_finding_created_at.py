# Generated by Django 5.1.3 on 2024-11-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_finding_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="finding",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]