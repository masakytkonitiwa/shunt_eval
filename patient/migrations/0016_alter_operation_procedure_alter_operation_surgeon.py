# Generated by Django 4.2.20 on 2025-04-04 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0015_alter_evaluation_motor_elbow_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='procedure',
            field=models.CharField(choices=[('AVF', 'AVF'), ('AVG', 'AVG'), ('PTA', 'PTA'), ('TPA', '血栓除去PTA'), ('OPTPA', '開創血栓除去PTA'), ('ETC', 'その他')], default='AVF', max_length=10, verbose_name='術式'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='surgeon',
            field=models.CharField(choices=[('HB', 'HB'), ('NG', 'NG'), ('ST', 'ST'), ('KB', 'KB'), ('ETC', 'ETC')], default='HB', max_length=100, verbose_name='術者'),
        ),
    ]
