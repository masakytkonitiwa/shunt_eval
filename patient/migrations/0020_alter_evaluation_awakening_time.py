# Generated by Django 4.2.20 on 2025-04-10 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0019_remove_evaluation_signer_evaluation_awakening_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='awakening_time',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='麻酔が覚めたと感じた時刻'),
        ),
    ]
