# Generated by Django 4.2.1 on 2023-06-02 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_leaveapplication_admin_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='checked_on',
            field=models.DateField(null=True),
        ),
    ]
