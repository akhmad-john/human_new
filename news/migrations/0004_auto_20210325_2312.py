# Generated by Django 2.2.19 on 2021-03-25 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20210325_2242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='ru_name',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='name',
            new_name='ru_name',
        ),
    ]
