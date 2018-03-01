# Generated by Django 2.0.2 on 2018-03-01 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='newest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='newest', to='comic.Episode'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='progress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='progress', to='comic.Episode'),
        ),
    ]
