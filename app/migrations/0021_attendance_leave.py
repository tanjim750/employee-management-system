# Generated by Django 4.2.1 on 2023-05-27 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_holiday_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='leave',
            field=models.BooleanField(default=False),
        ),
    ]
