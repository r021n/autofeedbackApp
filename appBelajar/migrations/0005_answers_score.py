# Generated by Django 4.2.9 on 2024-03-04 06:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appBelajar", "0004_questions_image_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="answers",
            name="score",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
