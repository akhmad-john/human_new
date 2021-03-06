# Generated by Django 2.2.19 on 2021-04-16 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0019_auto_20210407_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='oz_heading',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Оглавление(на латинице)'),
        ),
        migrations.AlterField(
            model_name='article',
            name='ru_heading',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Оглавление(на русском)'),
        ),
        migrations.AlterField(
            model_name='article',
            name='uz_heading',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Оглавление(на кирилице)'),
        ),
    ]
