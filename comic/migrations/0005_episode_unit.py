# Generated by Django 2.0.2 on 2018-03-26 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0004_auto_20180302_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='unit',
            field=models.CharField(default='話', max_length=10),
        ),
    ]
