# Generated by Django 2.2.19 on 2021-04-07 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(upload_to='ad_images', verbose_name='Рекламное фото')),
                ('ad_type', models.IntegerField(choices=[(1, 'Верх'), (2, 'Сбоку'), (3, 'Снизу')])),
                ('click_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Реклама',
                'verbose_name_plural': 'Реклама',
            },
        ),
    ]
