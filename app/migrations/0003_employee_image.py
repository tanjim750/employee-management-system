# Generated by Django 4.2.1 on 2023-05-20 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_employee_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='image',
            field=models.FileField(null=True, upload_to='images'),
        ),
    ]
