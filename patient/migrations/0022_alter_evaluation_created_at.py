# Generated by Django 4.2.20 on 2025-04-21 06:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0021_alter_operation_surgeon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
