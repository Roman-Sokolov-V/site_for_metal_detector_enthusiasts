# Generated by Django 5.1.3 on 2024-11-08 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_remove_collection_findings_finding_collections"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collection",
            options={
                "ordering": ("name",),
                "verbose_name": "Collection",
                "verbose_name_plural": "Collections",
            },
        ),
        migrations.AlterModelOptions(
            name="feedback",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "Feedback",
                "verbose_name_plural": "Feedbacks",
            },
        ),
        migrations.AlterModelOptions(
            name="finding",
            options={
                "ordering": ("-date_found", "-rating"),
                "verbose_name": "Finding",
                "verbose_name_plural": "Findings",
            },
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ("username",)},
        ),
        migrations.AddField(
            model_name="feedback",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]