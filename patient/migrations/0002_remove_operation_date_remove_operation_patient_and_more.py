# Generated by Django 4.2.11 on 2025-03-27 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation',
            name='date',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='patient',
        ),
        migrations.AddField(
            model_name='operation',
            name='age',
            field=models.PositiveIntegerField(default=0, verbose_name='年齢'),
        ),
        migrations.AddField(
            model_name='operation',
            name='gender',
            field=models.CharField(choices=[('M', '男性'), ('F', '女性')], default='M', max_length=1, verbose_name='性別'),
        ),
        migrations.AddField(
            model_name='operation',
            name='height',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='身長(cm)'),
        ),
        migrations.AddField(
            model_name='operation',
            name='procedure',
            field=models.CharField(choices=[('AVF', 'AVF'), ('AVG', 'AVG'), ('PTA', 'PTA'), ('TPA', '血栓除去PTA'), ('OPTPA', '開創血栓除去PTA')], default='AVF', max_length=10, verbose_name='術式'),
        ),
        migrations.AddField(
            model_name='operation',
            name='surgery_type',
            field=models.CharField(choices=[('P', 'プライマリー'), ('R', '再手術')], default='P', max_length=1, verbose_name='手術の種類'),
        ),
        migrations.AddField(
            model_name='operation',
            name='weight',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='体重(kg)'),
        ),
    ]
