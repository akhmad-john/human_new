# Generated by Django 2.2.19 on 2021-03-27 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20210325_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='oz_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='uz_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='oz_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='uz_name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]