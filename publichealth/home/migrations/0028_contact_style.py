# Generated by Django 2.1.13 on 2019-10-21 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_auto_20191017_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='style',
            field=models.TextField(blank=True, default=''),
        ),
    ]
