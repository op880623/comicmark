# Generated by Django 2.0.2 on 2018-04-25 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0005_episode_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='next',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='comic.Episode'),
        ),
    ]
