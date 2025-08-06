from django.conf import settings
from django.db import migrations, models
import api.models.character


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('archetype', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=50)),
                ('aiFilter', models.JSONField(default=api.models.character.default_ai_filter)),
                ('is_default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='characters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
