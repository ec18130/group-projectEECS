# Generated by Django 3.1.1 on 2020-12-07 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djnews', '0003_auto_20201207_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favourite_categories',
            field=models.ManyToManyField(blank=True, to='djnews.NewsCategory'),
        ),
    ]
