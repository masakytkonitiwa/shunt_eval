# Generated by Django 4.2.20 on 2025-04-08 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0018_alter_evaluation_motor_elbow_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='signer',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='awakening_time',
            field=models.CharField(blank=True, choices=[('11', '11時'), ('12', '12時'), ('13', '13時'), ('14', '14時'), ('15', '15時'), ('16', '16時'), ('17', '17時'), ('18', '18時'), ('19', '19時'), ('20', '20時'), ('21', '21時'), ('22', '22時'), ('23', '23時'), ('24', '24時'), ('25', '25時'), ('none', 'まだ自覚なし')], max_length=5, null=True, verbose_name='麻酔が覚めたと感じた時刻'),
        ),
    ]
