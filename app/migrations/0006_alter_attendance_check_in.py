# Generated by Django 4.2.1 on 2023-05-20 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_attendance_check_out_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='check_in',
            field=models.DateTimeField(),
        ),
    ]
