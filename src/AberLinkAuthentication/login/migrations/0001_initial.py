# Generated by Django 3.1.6 on 2021-02-09 14:56

from django.db import migrations, models
import login.models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordUser',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('last_login', models.DateTimeField(null=True)),
            ],
            managers=[
                ('objects', login.models.DiscordUserOAuth2Manager()),
            ],
        ),
    ]
