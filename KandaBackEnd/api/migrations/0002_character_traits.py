from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="character",
            name="physical_traits",
            field=models.JSONField(default=list, blank=True),
        ),
        migrations.AddField(
            model_name="character",
            name="personality_traits",
            field=models.JSONField(default=list, blank=True),
        ),
        migrations.AddField(
            model_name="character",
            name="background",
            field=models.TextField(blank=True, default=""),
        ),
    ]
