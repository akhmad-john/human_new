# Generated by Django 2.2.19 on 2021-04-06 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_auto_20210407_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='oz_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='uz_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
